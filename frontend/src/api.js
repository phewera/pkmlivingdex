import axios from 'axios';

const envUrl = import.meta.env.VITE_API_URL;
export const API_URL = envUrl !== undefined ? envUrl.trim() : `http://${window.location.hostname}:8000`;

export const api = axios.create({
    baseURL: API_URL,
});

export const getPokemon = async (generation) => {
    try {
        const response = await api.get('/pokemon', {
            params: { generation }
        });
        return response.data;
    } catch (error) {
        console.error("Error fetching pokemon", error);
        return [];
    }
};

export const updateCaptureStatus = async (pokemonId, caughtNormal, caughtShiny) => {
    try {
        const payload = {};
        if (caughtNormal !== undefined) payload.caught_normal = caughtNormal;
        if (caughtShiny !== undefined) payload.caught_shiny = caughtShiny;

        const response = await api.post(`/pokemon/${pokemonId}/capture`, null, {
            params: payload
        });
        return response.data;
    } catch (error) {
        console.error("Error updating capture status", error);
        return null; // Or throw
    }
};

export const getStats = async () => {
    try {
        const response = await api.get('/stats');
        return response.data;
    } catch (error) {
        console.error("Error fetching stats", error);
        return [];
    }
};

export const resetCollection = async () => {
    try {
        const response = await api.post('/progress/reset');
        return response.data;
    } catch (error) {
        console.error("Error resetting collection", error);
        return null;
    }
};
