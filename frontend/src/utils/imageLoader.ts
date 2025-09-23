/**
 * Gets the correct asset path based on the current environment
 * @param {string} path - The path to the asset (relative to /public folder)
 * @returns {string} The correct path to the asset
 */
export const getAssetPath = (path: string): string => {
  // Remove leading slash if present
  const cleanPath = path.startsWith('/') ? path.substring(1) : path;
  
  // In production, prepend /static/
  if (import.meta.env.PROD) {
    return `/static/${cleanPath}`.replace(/\/+/g, '/');
  }
  
  // In development, the public directory is served at the root
  return `/${cleanPath}`.replace(/\/+/g, '/');
};
