import React from 'react';

const StatisticsModal = ({ isOpen, onClose, stats, translations }) => {
    if (!isOpen) return null;

    // Calculate totals
    const totalCaught = stats.reduce((acc, curr) => acc + (curr.caught_any || 0), 0);
    const totalShiny = stats.reduce((acc, curr) => acc + (curr.caught_shiny || 0), 0);
    const totalAvailable = stats.reduce((acc, curr) => acc + curr.total, 0);
    const totalPercentage = totalAvailable > 0 ? Math.round((totalCaught / totalAvailable) * 1000) / 10 : 0;

    return (
        <div className="fixed inset-0 z-50 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
            {/* Backdrop */}
            <div
                className="fixed inset-0 bg-gray-900/50 backdrop-blur-sm transition-opacity"
                onClick={onClose}
            ></div>

            <div className="flex min-h-full items-center justify-center p-0 text-center sm:p-0">
                <div className="relative transform overflow-hidden rounded-2xl bg-white text-left shadow-xl transition-all w-[95%] sm:my-8 sm:w-full sm:max-w-2xl animate-in fade-in zoom-in-95 duration-300">

                    {/* Header */}
                    <div className="bg-red-600 px-4 py-3 sm:px-6 flex justify-between items-center">
                        <h3 className="text-lg font-black leading-6 text-white flex items-center gap-2" id="modal-title">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                            </svg>
                            {translations.statistics || "Statistics"}
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
                    <div className="px-4 py-5 sm:p-6 bg-gray-50 max-h-[70vh] overflow-y-auto custom-scrollbar">

                        {/* Global Overview Card */}
                        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-5 mb-6">
                            <h4 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-4">{translations.globalProgress || "Global Progress"}</h4>

                            <div className="grid grid-cols-3 gap-4 mb-4">
                                <div className="bg-blue-50 rounded-lg p-3 text-center">
                                    <span className="block text-xl sm:text-2xl font-black text-blue-600">{totalCaught}</span>
                                    <span className="text-[10px] sm:text-xs font-bold text-blue-400 uppercase">{translations.caught || "Caught"}</span>
                                </div>
                                <div className="bg-yellow-50 rounded-lg p-3 text-center">
                                    <span className="block text-xl sm:text-2xl font-black text-yellow-500">{totalShiny}</span>
                                    <span className="text-[10px] sm:text-xs font-bold text-yellow-600/70 uppercase">{translations.shiny || "Shiny"}</span>
                                </div>
                                <div className="bg-green-50 rounded-lg p-3 text-center">
                                    <span className="block text-xl sm:text-2xl font-black text-green-600">{totalPercentage}%</span>
                                    <span className="text-[10px] sm:text-xs font-bold text-green-500 uppercase">{translations.complete || "Complete"}</span>
                                </div>
                            </div>

                            {/* Global Progress Bar */}
                            <div className="w-full bg-gray-100 rounded-full h-3 overflow-hidden">
                                <div className="bg-blue-500 h-full transition-all duration-500" style={{ width: `${totalPercentage}%` }}></div>
                            </div>
                        </div>

                        {/* Generation Breakdown */}
                        <h4 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-3 px-1">{translations.byGeneration || "By Generation"}</h4>

                        <div className="space-y-3">
                            {stats.map((stat) => (
                                <div key={stat.generation} className="bg-white rounded-lg shadow-sm border border-gray-100 p-3 hover:border-gray-300 transition-colors">
                                    <div className="flex justify-between items-center mb-2">
                                        <span className="font-bold text-gray-800">{translations.genSuffix || "Gen"} {stat.generation}</span>
                                        <div className="flex items-center gap-3 text-sm">
                                            <span className="font-medium text-gray-600">{stat.caught_any} / {stat.total}</span>
                                            <span className="font-black text-blue-600">{stat.percentage_any}%</span>
                                        </div>
                                    </div>

                                    <div className="w-full bg-gray-100 rounded-full h-2 overflow-hidden flex relative">
                                        {/* Base progress (caught) */}
                                        <div className="bg-blue-500 h-full transition-all duration-500 absolute top-0 left-0" style={{ width: `${stat.percentage_any}%` }}></div>
                                        {/* Shiny overlay indicator (gold bar) */}
                                        {stat.percentage_shiny > 0 && (
                                            <div className="bg-yellow-400 h-full transition-all duration-500 absolute top-0 left-0 opacity-80" style={{ width: `${stat.percentage_shiny}%` }}></div>
                                        )}
                                    </div>
                                    {/* Shiny count if any */}
                                    {stat.caught_shiny > 0 && (
                                        <div className="flex justify-end mt-1">
                                            <span className="text-[10px] font-bold text-yellow-600 bg-yellow-50 px-1.5 py-0.5 rounded-full border border-yellow-100">
                                                ★ {stat.caught_shiny}
                                            </span>
                                        </div>
                                    )}
                                </div>
                            ))}
                        </div>

                    </div>

                    {/* Footer */}
                    <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse border-t border-gray-100">
                        <button
                            type="button"
                            className="mt-3 w-full inline-flex justify-center rounded-lg border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-bold text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm transition-colors cursor-pointer"
                            onClick={onClose}
                        >
                            {translations.close || "Close"}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default StatisticsModal;
