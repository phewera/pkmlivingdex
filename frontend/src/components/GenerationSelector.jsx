import React, { useState, useRef, useEffect } from 'react';

const GenerationSelector = ({ selectedGeneration, onSelect, translations }) => {
    const [isOpen, setIsOpen] = useState(false);
    const dropdownRef = useRef(null);

    // Close dropdown when clicking outside
    useEffect(() => {
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setIsOpen(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, []);

    const handleSelect = (gen) => {
        onSelect(gen);
        setIsOpen(false);
    };

    const generations = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9];

    return (
        <div className="relative" ref={dropdownRef}>
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="flex items-center justify-between w-full bg-red-700 hover:bg-red-800 text-white text-xs sm:text-sm font-bold py-2 pl-3 sm:pl-4 pr-3 rounded-lg shadow-sm transition-all duration-200 outline-none focus:ring-2 focus:ring-white/50"
            >
                <span className="truncate mr-2">
                    {selectedGeneration === 0
                        ? translations.allGens
                        : `${translations.genSuffix} ${selectedGeneration}`}
                </span>
                <svg
                    className={`h-4 w-4 text-white/80 transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M19 9l-7 7-7-7" />
                </svg>
            </button>

            {/* Dropdown Menu */}
            {isOpen && (
                <div className="absolute top-full left-0 mt-2 w-full min-w-[160px] bg-white rounded-xl shadow-xl border border-gray-100 py-1 z-50 animate-in fade-in zoom-in-95 duration-200 origin-top overflow-hidden">
                    <div className="py-1">
                        {generations.map((gen) => (
                            <button
                                key={gen}
                                onClick={() => handleSelect(gen)}
                                className={`w-full text-left px-4 py-2.5 text-sm font-medium transition-colors duration-150
                  ${selectedGeneration === gen
                                        ? 'bg-red-50 text-red-700 font-bold'
                                        : 'text-gray-700 hover:bg-gray-50 hover:text-red-600'
                                    }
                `}
                            >
                                {gen === 0 ? translations.allGens : `${translations.genSuffix} ${gen}`}
                            </button>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default GenerationSelector;
