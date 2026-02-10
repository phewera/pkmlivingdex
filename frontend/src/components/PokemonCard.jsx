import React from 'react';
import { API_URL } from '../api';

const PokemonCard = ({ pokemon, onUpdate, language }) => {
    const handleNormalChange = () => {
        onUpdate(pokemon.id, !pokemon.caught_normal, undefined);
    };

    const handleShinyChange = () => {
        onUpdate(pokemon.id, undefined, !pokemon.caught_shiny);
    };

    const displayName = language === 'en' ? pokemon.name_en : pokemon.name;

    const getImageUrl = () => {
        const path = pokemon.caught_shiny ? pokemon.shiny_image_url : pokemon.image_url;
        // If it's a relative path (starting with /), prefix with API_URL
        if (path && path.startsWith('/')) {
            return `${API_URL}${path}`;
        }
        return path;
    };

    return (
        <div className={`p-3 sm:p-4 rounded-xl shadow-lg flex flex-col items-center transition-all duration-300 border-2 ${(pokemon.caught_normal || pokemon.caught_shiny) ? 'bg-green-50 border-green-200' : 'bg-white border-gray-100'}`}>
            <div className="text-gray-400 text-[10px] sm:text-xs font-mono mb-0.5 sm:mb-1">#{pokemon.id.toString().padStart(4, '0')}</div>
            <h3 className="text-sm sm:text-lg font-bold capitalize text-gray-800 mb-1 sm:mb-2 truncate w-full text-center px-1" title={displayName}>{displayName}</h3>

            <div className="relative cursor-pointer group" onClick={handleNormalChange}>
                <img
                    src={getImageUrl()}
                    alt={displayName}
                    className={`w-20 h-20 sm:w-28 sm:h-28 object-contain transition-all duration-300 ${(pokemon.caught_normal || pokemon.caught_shiny) ? 'opacity-100 scale-110' : 'opacity-40 grayscale group-hover:grayscale-0 group-hover:opacity-60'}`}
                />
            </div>

            <div className="flex gap-1.5 sm:gap-2 w-full mt-3 sm:mt-4">
                <button
                    onClick={(e) => { e.stopPropagation(); handleNormalChange(); }}
                    className={`flex-1 py-1 sm:py-1.5 px-1 sm:px-2 rounded-lg text-[10px] sm:text-xs font-bold transition-all border-b-2 ${pokemon.caught_normal
                        ? 'bg-blue-600 text-white shadow-md border-blue-800'
                        : 'bg-gray-100 text-gray-400 hover:bg-gray-200 border-transparent'
                        }`}
                >
                    Normal
                </button>
                <button
                    onClick={(e) => { e.stopPropagation(); handleShinyChange(); }}
                    className={`flex-1 py-1 sm:py-1.5 px-1 sm:px-2 rounded-lg text-[10px] sm:text-xs font-bold transition-all border-b-2 ${pokemon.caught_shiny
                        ? 'bg-yellow-400 text-white shadow-md border-yellow-600'
                        : 'bg-gray-100 text-gray-400 hover:bg-gray-200 border-transparent'
                        }`}
                >
                    Shiny
                </button>
            </div>
        </div>
    );
};

export default PokemonCard;

