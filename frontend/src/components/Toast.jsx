import React, { useEffect } from 'react';

function Toast({ message, visible, onClose }) {
    useEffect(() => {
        if (visible) {
            const timer = setTimeout(() => {
                onClose();
            }, 3000);
            return () => clearTimeout(timer);
        }
    }, [visible, onClose]);

    if (!visible) return null;

    return (
        <div className="fixed bottom-6 left-1/2 -translate-x-1/2 sm:left-auto sm:translate-x-0 sm:right-6 z-[100] w-max max-w-[90vw] sm:max-w-md animate-in slide-in-from-bottom-4 fade-in duration-300">
            <div className="bg-gray-900/90 backdrop-blur text-white px-6 py-3 rounded-2xl shadow-2xl flex items-center gap-3 border border-white/10">
                <div className="w-6 h-6 bg-green-500 rounded-full flex items-center justify-center">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                    </svg>
                </div>
                <span className="font-medium text-sm sm:text-base">{message}</span>
                <button
                    onClick={onClose}
                    className="ml-2 text-gray-400 hover:text-white transition-colors"
                >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>
        </div>
    );
}

export default Toast;
