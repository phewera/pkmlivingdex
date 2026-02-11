import React, { useRef, useState, useEffect } from 'react';
import { translations } from '../translations';
import { resetCollection, API_URL } from '../api';
import ConfirmationModal from './ConfirmationModal';

function SettingsModal({ isOpen, onClose, language, setLanguage, onImportSuccess, showToast }) {
    const fileInputRef = useRef(null);
    const [showResetConfirm, setShowResetConfirm] = useState(false);
    const [tempLanguage, setTempLanguage] = useState(language);
    const [isImporting, setIsImporting] = useState(false);
    const [importProgress, setImportProgress] = useState(0);
    const [isUpdating, setIsUpdating] = useState(false);
    const [updateStatus, setUpdateStatus] = useState({ progress: 0, message: "" });
    const updateIntervalRef = useRef(null);
    const t = translations[tempLanguage] || translations['de'];

    // Sync tempLanguage when modal opens
    useEffect(() => {
        if (isOpen) {
            setTempLanguage(language);
        }
        return () => {
            if (updateIntervalRef.current) clearInterval(updateIntervalRef.current);
        };
    }, [isOpen, language]);

    if (!isOpen) return null;

    const handleExport = async () => {
        try {
            const response = await fetch(`${API_URL}/export/csv`, {
                method: 'GET',
            });

            if (!response.ok) throw new Error('Export failed');

            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;

            // Generate filename with timestamp
            const date = new Date();
            const timestamp = date.toISOString().replace(/[:.]/g, '-').slice(0, 19);
            a.download = `pokemon_living_dex_${timestamp}.csv`;

            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);

            showToast(t.exportSuccess);
        } catch (error) {
            console.error('Export exception:', error);
            showToast(t.importError); // Reusing import error message for now, ideally specific export error
        }
    };

    const handleImport = async (event) => {
        const file = event.target.files[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        setIsImporting(true);
        setImportProgress(10);

        // Simulated progress interval
        const progressInterval = setInterval(() => {
            setImportProgress(prev => {
                if (prev >= 90) return prev;
                return prev + 5;
            });
        }, 200);

        try {
            const response = await fetch(`${API_URL}/import/csv`, {
                method: 'POST',
                body: formData,
            });

            clearInterval(progressInterval);

            if (response.ok) {
                setImportProgress(100);
                setTimeout(() => {
                    showToast(t.importSuccess);
                    onImportSuccess();
                    setIsImporting(false);
                    setImportProgress(0);
                }, 500);
            } else {
                showToast(t.importError);
                setIsImporting(false);
                setImportProgress(0);
            }
        } catch (error) {
            clearInterval(progressInterval);
            console.error('Import failed', error);
            showToast(t.importError);
            setIsImporting(false);
            setImportProgress(0);
        }
    };

    const handleReset = () => {
        setShowResetConfirm(true);
    };

    const finalizeReset = async () => {
        try {
            const response = await resetCollection();
            if (response) {
                onImportSuccess(); // We use this callback to refresh the main view
                showToast(t.resetSuccess);
            }
        } catch (error) {
            console.error('Reset failed', error);
        }
    };

    const handleSave = () => {
        if (tempLanguage !== language) {
            setLanguage(tempLanguage);
            showToast(translations[tempLanguage].settingsSaved);
        }
        onClose();
    };

    const handleUpdateDatabase = async () => {
        try {
            const startResponse = await fetch(`${API_URL}/system/update-database`, { method: 'POST' });
            if (!startResponse.ok) throw new Error("Failed to start update");

            setIsUpdating(true);
            setUpdateStatus({ progress: 0, message: "Starting..." });

            updateIntervalRef.current = setInterval(async () => {
                try {
                    const statusRes = await fetch(`${API_URL}/system/update-status`);
                    const status = await statusRes.json();

                    setUpdateStatus(status);

                    if (status.state === 'complete') {
                        clearInterval(updateIntervalRef.current);
                        setIsUpdating(false);
                        showToast(t.updateCompleted || "Update complete!");
                        if (onImportSuccess) onImportSuccess();
                    } else if (status.state === 'error') {
                        clearInterval(updateIntervalRef.current);
                        setIsUpdating(false);
                        showToast(t.updateError || status.message || "Update failed");
                    }
                } catch (e) {
                    console.error("Poll error", e);
                }
            }, 1000);

        } catch (error) {
            console.error("Update start failed", error);
            showToast(t.updateError || "Failed to start update");
        }
    };

    return (
        <>
            <div className="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
                {/* Backdrop */}
                <div
                    className="fixed inset-0 bg-gray-900/50 backdrop-blur-sm transition-opacity"
                    onClick={onClose}
                ></div>

                <div className="flex min-h-full items-center justify-center p-0 text-center sm:p-0">
                    <div className="relative transform overflow-hidden rounded-2xl bg-white text-left shadow-xl transition-all w-[95%] sm:my-8 sm:w-full sm:max-w-md animate-in fade-in zoom-in-95 duration-300">

                        {/* Header */}
                        <div className="bg-red-600 px-4 py-3 sm:px-6 flex justify-between items-center">
                            <h3 className="text-lg font-black leading-6 text-white flex items-center gap-2" id="modal-title">
                                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37a1.724 1.724 0 002.572-1.065z" />
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                </svg>
                                {t.settings}
                            </h3>
                            <button
                                onClick={onClose}
                                className="rounded-lg p-1 text-red-100 hover:bg-red-700 hover:text-white transition-colors focus:outline-none focus:ring-2 focus:ring-white"
                            >
                                <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
                                </svg>
                            </button>
                        </div>

                        {/* Body */}
                        <div className="px-4 py-5 sm:p-6 bg-gray-50 space-y-6">

                            {/* Language Group */}
                            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
                                <label className="block text-sm font-bold text-gray-500 uppercase tracking-wider mb-3">{t.language}</label>
                                <div className="flex bg-gray-100 p-1 rounded-xl">
                                    <button
                                        onClick={() => setTempLanguage('de')}
                                        className={`flex-1 py-2 rounded-lg font-bold transition-all ${tempLanguage === 'de' ? 'bg-white shadow text-red-600' : 'text-gray-500 hover:text-gray-700'}`}
                                    >
                                        Deutsch
                                    </button>
                                    <button
                                        onClick={() => setTempLanguage('en')}
                                        className={`flex-1 py-2 rounded-lg font-bold transition-all ${tempLanguage === 'en' ? 'bg-white shadow text-red-600' : 'text-gray-500 hover:text-gray-700'}`}
                                    >
                                        English
                                    </button>
                                </div>
                            </div>

                            {/* Data Management Group */}
                            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
                                <label className="block text-sm font-bold text-gray-500 uppercase tracking-wider mb-3">{t.dataManagement || "Data Management"}</label>
                                <div className="grid grid-cols-2 gap-4">
                                    <button
                                        onClick={handleExport}
                                        className="flex flex-col items-center justify-center p-4 rounded-xl bg-blue-50 text-blue-700 hover:bg-blue-100 transition-colors border border-transparent hover:border-blue-200"
                                    >
                                        <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a2 2 0 002 2h12a2 2 0 002-2v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                                        </svg>
                                        <span className="text-sm font-bold">{t.exportCsv}</span>
                                    </button>

                                    <button
                                        onClick={() => fileInputRef.current.click()}
                                        className="flex flex-col items-center justify-center p-4 rounded-xl bg-green-50 text-green-700 hover:bg-green-100 transition-colors border border-transparent hover:border-green-200"
                                    >
                                        <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a2 2 0 002 2h12a2 2 0 002-2v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                                        </svg>
                                        <span className="text-sm font-bold">{t.importCsv}</span>
                                    </button>
                                    <input
                                        type="file"
                                        ref={fileInputRef}
                                        onChange={handleImport}
                                        accept=".csv"
                                        className="hidden"
                                    />

                                    <button
                                        onClick={handleUpdateDatabase}
                                        disabled={isUpdating}
                                        className={`col-span-2 flex flex-col items-center justify-center p-4 rounded-xl transition-colors border border-transparent ${isUpdating ? 'bg-gray-100 text-gray-400 cursor-not-allowed' : 'bg-purple-50 text-purple-700 hover:bg-purple-100 hover:border-purple-200'}`}
                                    >
                                        <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                                        </svg>
                                        <span className="text-sm font-bold">{isUpdating ? (t.updating || "Updating...") : (t.updateDatabase || "Update Database")}</span>
                                    </button>
                                </div>

                                {isUpdating && (
                                    <div className="mt-4">
                                        <div className="flex justify-between items-center mb-1">
                                            <span className="text-xs font-bold text-gray-400 uppercase tracking-tighter">
                                                {(() => {
                                                    if (!updateStatus.message) return "Working...";
                                                    const parts = updateStatus.message.split('|');
                                                    const key = parts[0];
                                                    const param = parts[1];

                                                    let msg = t[key] || updateStatus.message;
                                                    if (param && msg.includes(":")) {
                                                        return msg + param;
                                                    }
                                                    return msg;
                                                })()}
                                            </span>
                                            <span className="text-xs font-bold text-purple-600">{updateStatus.progress}%</span>
                                        </div>
                                        <div className="w-full bg-gray-100 rounded-full h-2 overflow-hidden shadow-inner">
                                            <div
                                                className="bg-purple-600 h-full transition-all duration-300 ease-out"
                                                style={{ width: `${updateStatus.progress}%` }}
                                            ></div>
                                        </div>
                                    </div>
                                )}

                                {isImporting && (
                                    <div className="mt-4">
                                        <div className="flex justify-between items-center mb-1">
                                            <span className="text-xs font-bold text-gray-400 uppercase tracking-tighter">Importing...</span>
                                            <span className="text-xs font-bold text-red-500">{importProgress}%</span>
                                        </div>
                                        <div className="w-full bg-gray-100 rounded-full h-2 overflow-hidden shadow-inner">
                                            <div
                                                className="bg-red-500 h-full transition-all duration-300 ease-out"
                                                style={{ width: `${importProgress}%` }}
                                            ></div>
                                        </div>
                                    </div>
                                )}
                            </div>

                            {/* Danger Zone */}
                            <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4">
                                <button
                                    onClick={handleReset}
                                    className="w-full flex items-center justify-center gap-2 p-3 rounded-xl bg-red-50 text-red-600 hover:bg-red-100 transition-colors border border-transparent hover:border-red-200"
                                >
                                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                                    </svg>
                                    <span className="text-sm font-bold">{t.resetCollection}</span>
                                </button>
                            </div>

                        </div>

                        {/* Footer */}
                        <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse border-t border-gray-100">
                            <button
                                onClick={handleSave}
                                className="w-full inline-flex justify-center rounded-lg border border-transparent shadow-sm px-4 py-2 bg-gray-800 text-base font-bold text-white hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 sm:ml-3 sm:w-auto sm:text-sm transition-colors"
                            >
                                {t.save || "Save"}
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <ConfirmationModal
                isOpen={showResetConfirm}
                onClose={() => setShowResetConfirm(false)}
                onConfirm={finalizeReset}
                message={t.resetConfirm}
                language={tempLanguage}
            />
        </>
    );
}

export default SettingsModal;
