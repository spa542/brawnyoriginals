/**
 * Returns the base URL for API requests based on the environment.
 * @returns {string} The base URL for API requests.
 */
export const getBaseUrl = () => {
    return import.meta.env.PROD ? '' : 'http://localhost:8000';
}