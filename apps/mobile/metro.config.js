const { getDefaultConfig } = require('expo/metro-config');

const config = getDefaultConfig(__dirname);

// Solucionar problemas de bloqueo en Windows
config.resolver.assetExts = config.resolver.assetExts.filter(
  ext => ext !== 'svg'
);
config.resolver.sourceExts.push('svg');

// Limitar workers para evitar bloqueos
config.maxWorkers = 1;

module.exports = config;
