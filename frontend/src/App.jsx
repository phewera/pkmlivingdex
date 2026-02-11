import React, { useState, useEffect } from 'react';
import { getPokemon, updateCaptureStatus, getStats } from './api';
import PokemonCard from './components/PokemonCard';
import SettingsModal from './components/SettingsModal';
import StatisticsModal from './components/StatisticsModal';
import GenerationSelector from './components/GenerationSelector';
import Toast from './components/Toast';
import { translations } from './translations';

const round = (value, precision) => {
  const multiplier = Math.pow(10, precision || 0);
  return Math.round(value * multiplier) / multiplier;
};

const ProgressPills = ({ activeStats, t, className = "" }) => (
  <div className={`flex items-center gap-4 ${className}`}>
    <div className="flex items-center gap-2">
      <div className="w-12 sm:w-24 bg-red-800 rounded-full h-1.5 sm:h-2.5 overflow-hidden">
        <div className="bg-white h-full transition-all duration-500 shadow-[0_0_8px_rgba(255,255,255,0.5)]" style={{ width: `${activeStats.percentage_any}%` }}></div>
      </div>
      <div className="flex flex-col">
        <span className="text-[9px] sm:text-[11px] font-bold opacity-80 uppercase leading-none">{t.caught}</span>
        <span className="text-[10px] sm:text-[13px] font-black leading-none mt-1">{activeStats.percentage_any}%</span>
      </div>
    </div>
    <div className="flex items-center gap-2">
      <div className="w-12 sm:w-24 bg-red-800 rounded-full h-1.5 sm:h-2.5 overflow-hidden">
        <div className="bg-yellow-400 h-full transition-all duration-500 shadow-[0_0_8px_rgba(250,204,21,0.4)]" style={{ width: `${activeStats.percentage_shiny}%` }}></div>
      </div>
      <div className="flex flex-col">
        <span className="text-[9px] sm:text-[11px] font-bold opacity-80 uppercase leading-none">{t.shiny}</span>
        <span className="text-[10px] sm:text-[13px] font-black leading-none mt-1">{activeStats.percentage_shiny}%</span>
      </div>
    </div>
  </div>
);

function App() {
  const [pokemonList, setPokemonList] = useState([]);
  const [stats, setStats] = useState([]);
  const [selectedGeneration, setSelectedGeneration] = useState(1);
  const [loading, setLoading] = useState(false);
  const [language, setLanguage] = useState(() => {
    const saved = localStorage.getItem('language');
    return (saved === 'en' || saved === 'de') ? saved : 'de';
  });
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [isStatsOpen, setIsStatsOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterType, setFilterType] = useState('all'); // all, uncaught, shiny_missing
  const [toast, setToast] = useState({ visible: false, message: '' });

  const t = translations[language];

  const showToast = (message) => setToast({ visible: true, message });
  const hideToast = () => setToast({ ...toast, visible: false });

  const filteredPokemon = React.useMemo(() => {
    return pokemonList.filter(p => {
      const pName = language === 'en' ? (p.name_en || p.name) : p.name;
      const name = (pName || '').toLowerCase();
      const matchesSearch = name.includes(searchQuery.toLowerCase()) || p.id.toString().includes(searchQuery);

      if (!matchesSearch) return false;

      if (filterType === 'uncaught') return !p.caught_normal && !p.caught_shiny;
      if (filterType === 'shiny_missing') return !p.caught_shiny;

      return true;
    });
  }, [pokemonList, searchQuery, filterType, language]);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 300);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    localStorage.setItem('language', language);
  }, [language]);

  useEffect(() => {
    fetchStats();
    fetchPokemon(selectedGeneration);
  }, [selectedGeneration]);

  const fetchStats = async () => {
    const data = await getStats();
    setStats(data);
  };

  const fetchPokemon = async (gen) => {
    setLoading(true);
    // 0 means all generations
    const data = await getPokemon(gen === 0 ? undefined : gen);
    setPokemonList(data);
    setLoading(false);
  };

  const handleUpdate = async (id, caughtNormal, caughtShiny) => {
    try {
      await updateCaptureStatus(id, caughtNormal, caughtShiny);
      // Optimistic update
      setPokemonList(prevList => prevList.map(p => {
        if (p.id === id) {
          return {
            ...p,
            caught_normal: caughtNormal !== undefined ? caughtNormal : p.caught_normal,
            caught_shiny: caughtShiny !== undefined ? caughtShiny : p.caught_shiny
          };
        }
        return p;
      }));
      fetchStats(); // Update stats in background
    } catch (e) {
      // Error handling without excessive logging
    }
  };

  const handleImportSuccess = () => {
    fetchStats();
    fetchPokemon(selectedGeneration);
  };

  const totalStats = stats.reduce((acc, curr) => {
    acc.total += curr.total;
    acc.caught_any += curr.caught_any || 0;
    acc.caught_normal += curr.caught_normal;
    acc.caught_shiny += curr.caught_shiny;
    return acc;
  }, { total: 0, caught_any: 0, caught_normal: 0, caught_shiny: 0 });

  const totalPercentageAny = totalStats.total > 0 ? round((totalStats.caught_any / totalStats.total) * 100, 1) : 0;
  const totalPercentageShiny = totalStats.total > 0 ? round((totalStats.caught_shiny / totalStats.total) * 100, 1) : 0;

  const currentGenStats = stats.find(s => s.generation === selectedGeneration);

  const activeStats = selectedGeneration === 0 ? {
    percentage_any: totalPercentageAny,
    percentage_shiny: totalPercentageShiny,
    caught_any: totalStats.caught_any,
    total: totalStats.total
  } : {
    percentage_any: currentGenStats?.percentage_any || 0,
    percentage_shiny: currentGenStats?.percentage_shiny || 0,
    caught_any: currentGenStats?.caught_any || 0,
    total: currentGenStats?.total || 0
  };

  return (
    <div className="min-h-screen bg-gray-50 text-gray-800 font-sans">
      <header className={`bg-red-600 text-white shadow-md sticky top-0 z-30 transition-all duration-300 py-3 ${isScrolled ? 'lg:py-3' : 'lg:py-5'}`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6">

          {/* Desktop Layout (Hidden on mobile) */}
          <div className="hidden lg:flex justify-between items-center gap-4">
            <div className="flex items-center gap-4 shrink-0">
              <h1 className={`${isScrolled ? 'text-xl' : 'text-2xl'} font-black tracking-tight transition-all duration-300`}>
                Pokémon Living Dex
              </h1>

              <div
                className={`transition-all duration-500 ease-in-out transform origin-left ${isScrolled
                  ? 'opacity-100 translate-x-0'
                  : 'opacity-0 -translate-x-4 pointer-events-none'
                  }`}
              >
                {isScrolled && (
                  <div className="px-4 border-l border-red-400 h-8 flex items-center">
                    <ProgressPills activeStats={activeStats} t={t} />
                  </div>
                )}
              </div>
            </div>

            <div className="flex items-center gap-3 shrink-0">
              <div className="relative w-48 md:w-56 z-50">
                <GenerationSelector
                  selectedGeneration={selectedGeneration}
                  onSelect={setSelectedGeneration}
                  translations={t}
                  availableGenerations={stats.map(s => s.generation).sort((a, b) => a - b)}
                />
              </div>

              <button
                onClick={() => setIsStatsOpen(true)}
                className="p-2 hover:bg-red-700 rounded-lg transition-colors shrink-0"
                title={t.statistics}
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </button>

              <button
                onClick={() => setIsSettingsOpen(true)}
                className="p-2 hover:bg-red-700 rounded-lg transition-colors shrink-0"
                title={t.settings}
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37a1.724 1.724 0 002.572-1.065z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </button>
            </div>
          </div>

          {/* Mobile Layout (Visible only on mobile) */}
          <div className="lg:hidden flex flex-col gap-3">
            {/* Row 1: Title + Settings */}
            <div className="flex justify-between items-center">
              <h1 className="text-xl font-black tracking-tight">
                Pokémon Living Dex
              </h1>
              <div className="flex items-center gap-1">
                <button
                  onClick={() => setIsStatsOpen(true)}
                  className="p-2 hover:bg-red-700 rounded-lg transition-colors"
                  title={t.statistics}
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </button>
                <button
                  onClick={() => setIsSettingsOpen(true)}
                  className="p-2 hover:bg-red-700 rounded-lg transition-colors"
                  title={t.settings}
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37a1.724 1.724 0 002.572-1.065z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                </button>
              </div>
            </div>

            {/* Row 2: Gen Select + Progress */}
            <div className="flex justify-between items-center gap-2">
              <div className="relative w-40 shrink-0 z-40">
                <GenerationSelector
                  selectedGeneration={selectedGeneration}
                  onSelect={setSelectedGeneration}
                  translations={t}
                  availableGenerations={stats.map(s => s.generation).sort((a, b) => a - b)}
                />
              </div>

              {/* Reused Progress Pills */}
              <div className="flex-1 flex justify-end overflow-hidden">
                <div
                  className={`transition-all duration-500 ease-in-out transform origin-right whitespace-nowrap ${isScrolled
                    ? 'opacity-100 translate-x-0'
                    : 'opacity-0 translate-x-4 pointer-events-none'
                    }`}
                >
                  <ProgressPills activeStats={activeStats} t={t} className="scale-90 origin-right" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto p-6 space-y-6">
        {/* Global Progress Section */}
        {selectedGeneration === 0 && (
          <section className="bg-white p-5 rounded-2xl shadow-sm border border-gray-100">
            <div className="flex flex-col md:flex-row md:justify-between md:items-center items-start gap-2 md:gap-0 mb-4">
              <h2 className="text-lg font-black text-gray-900 flex items-center gap-2">
                <span className="p-1.5 bg-red-100 text-red-600 rounded-lg">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </span>
                {t.globalProgress}
              </h2>
              <div className="text-gray-500 font-bold bg-gray-50 px-4 py-1.5 rounded-full text-xs sm:text-sm border border-gray-100">
                {totalStats.caught_any} / {totalStats.total} {t.captured}
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-4">
              <div className="space-y-2.5">
                <div className="flex justify-between items-end">
                  <span className="text-xs sm:text-sm font-bold text-gray-400 uppercase tracking-widest">{t.caught}</span>
                  <span className="text-base sm:text-xl font-black text-blue-600">{totalPercentageAny}%</span>
                </div>
                <div className="w-full bg-gray-100 rounded-full h-2.5 sm:h-4 overflow-hidden border border-gray-100 shadow-inner">
                  <div
                    className="bg-gradient-to-r from-blue-500 to-blue-600 h-full rounded-full transition-all duration-700 ease-out shadow-[inset_0_2px_4px_rgba(0,0,0,0.1)]"
                    style={{ width: `${totalPercentageAny}%` }}
                  ></div>
                </div>
              </div>

              <div className="space-y-2.5">
                <div className="flex justify-between items-end">
                  <span className="text-xs sm:text-sm font-bold text-gray-400 uppercase tracking-widest">{t.shiny}</span>
                  <span className="text-base sm:text-xl font-black text-yellow-500">{totalPercentageShiny}%</span>
                </div>
                <div className="w-full bg-gray-100 rounded-full h-2.5 sm:h-4 overflow-hidden border border-gray-100 shadow-inner">
                  <div
                    className="bg-gradient-to-r from-yellow-300 to-yellow-500 h-full rounded-full transition-all duration-700 ease-out shadow-[inset_0_2px_4px_rgba(0,0,0,0.1)]"
                    style={{ width: `${totalPercentageShiny}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </section>
        )}

        {/* Generation Progress Section */}
        {selectedGeneration !== 0 && currentGenStats && (
          <section className="bg-white p-5 rounded-2xl shadow-sm border border-gray-100">
            <div className="flex flex-col md:flex-row md:justify-between md:items-center items-start gap-2 md:gap-0 mb-4">
              <h2 className="text-lg font-black text-gray-900 flex items-center gap-2">
                <span className="p-1.5 bg-red-100 text-red-600 rounded-lg">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </span>
                {t.genSuffix} {selectedGeneration} {t.progress}
              </h2>
              <div className="text-gray-500 font-bold bg-gray-50 px-4 py-1.5 rounded-full text-xs sm:text-sm border border-gray-100">
                {currentGenStats.caught_any} / {currentGenStats.total} {t.captured}
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-4">
              <div className="space-y-2.5">
                <div className="flex justify-between items-end">
                  <span className="text-xs sm:text-sm font-bold text-gray-400 uppercase tracking-widest">{t.caught}</span>
                  <span className="text-base sm:text-xl font-black text-blue-600">{currentGenStats.percentage_any}%</span>
                </div>
                <div className="w-full bg-gray-100 rounded-full h-2.5 sm:h-4 overflow-hidden border border-gray-100 shadow-inner">
                  <div
                    className="bg-gradient-to-r from-blue-500 to-blue-600 h-full rounded-full transition-all duration-700 ease-out shadow-[inset_0_2px_4px_rgba(0,0,0,0.1)]"
                    style={{ width: `${currentGenStats.percentage_any}%` }}
                  ></div>
                </div>
              </div>

              <div className="space-y-2.5">
                <div className="flex justify-between items-end">
                  <span className="text-xs sm:text-sm font-bold text-gray-400 uppercase tracking-widest">{t.shiny}</span>
                  <span className="text-base sm:text-xl font-black text-yellow-500">{currentGenStats.percentage_shiny}%</span>
                </div>
                <div className="w-full bg-gray-100 rounded-full h-2.5 sm:h-4 overflow-hidden border border-gray-100 shadow-inner">
                  <div
                    className="bg-gradient-to-r from-yellow-300 to-yellow-500 h-full rounded-full transition-all duration-700 ease-out shadow-[inset_0_2px_4px_rgba(0,0,0,0.1)]"
                    style={{ width: `${currentGenStats.percentage_shiny}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </section>
        )}

        {/* Search and Filters */}
        <section className="bg-white p-4 rounded-2xl shadow-sm border border-gray-100 flex flex-col md:flex-row gap-4">
          <div className="relative flex-1">
            <input
              type="text"
              placeholder={t.searchPlaceholder}
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full bg-gray-50 border border-gray-200 rounded-xl py-2.5 pl-10 pr-4 text-sm focus:ring-2 focus:ring-red-500/20 focus:border-red-500 outline-none transition-all font-medium"
            />
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-gray-400">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
          </div>

          <div className="flex gap-2 shrink-0">
            <button
              onClick={() => setFilterType('all')}
              className={`px-4 py-2 rounded-xl text-xs sm:text-sm font-bold transition-all ${filterType === 'all' ? 'bg-gray-800 text-white shadow-md' : 'bg-gray-50 text-gray-500 hover:bg-gray-100'}`}
            >
              {t.all}
            </button>
            <button
              onClick={() => setFilterType('uncaught')}
              className={`px-4 py-2 rounded-xl text-xs sm:text-sm font-bold transition-all ${filterType === 'uncaught' ? 'bg-blue-600 text-white shadow-md' : 'bg-gray-50 text-gray-500 hover:bg-gray-100'}`}
            >
              {t.missing}
            </button>
            <button
              onClick={() => setFilterType('shiny_missing')}
              className={`px-4 py-2 rounded-xl text-xs sm:text-sm font-bold transition-all ${filterType === 'shiny_missing' ? 'bg-yellow-500 text-white shadow-md' : 'bg-gray-50 text-gray-500 hover:bg-gray-100'}`}
            >
              {t.shinyMissing}
            </button>
            <button
              onClick={() => {
                setSearchQuery('');
                setFilterType('all');
              }}
              className={`p-2.5 rounded-xl transition-all flex items-center justify-center border border-transparent ${(searchQuery || filterType !== 'all') ? 'text-red-600 hover:bg-red-50 hover:border-red-100' : 'text-gray-300 cursor-default hover:bg-gray-50'}`}
              title={t.reset}
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </section>

        {/* Pokemon Grid */}
        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-600"></div>
          </div>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-3 sm:gap-4">
            {filteredPokemon.map(poke => (
              <PokemonCard key={poke.id} pokemon={poke} onUpdate={handleUpdate} language={language} />
            ))}
          </div>
        )}
      </main>

      <SettingsModal
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
        language={language}
        setLanguage={setLanguage}
        showToast={showToast}
        onImportSuccess={handleImportSuccess}
      />

      <StatisticsModal
        isOpen={isStatsOpen}
        onClose={() => setIsStatsOpen(false)}
        stats={stats}
        translations={t}
      />

      <Toast
        message={toast.message}
        visible={toast.visible}
        onClose={hideToast}
      />
    </div>
  );
}

export default App;
