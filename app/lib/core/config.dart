/// FoundryOS App Config — env via --dart-define, never hard-coded.
/// Backend is source of truth for LLM; app only needs API URL.
/// Baseten key stays server-side only.
class AppConfig {
  // Passed via: flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8000 --dart-define=LLM_MODE=live
  static const apiBaseUrl = String.fromEnvironment('API_BASE_URL', defaultValue: 'http://localhost:8000');
  static const llmMode = String.fromEnvironment('LLM_MODE', defaultValue: 'mock');
  // Never store Baseten key in app; this is just for UI badge when backend injects via dart-define
  static const basetenKeyPresent = String.fromEnvironment('BASETEN_API_KEY', defaultValue: '');
  static bool get isLive => llmMode == 'live' || basetenKeyPresent.isNotEmpty;
  static bool get isMock => !isLive;

  // Baseten endpoint info (display only, actual calls via backend)
  static const basetenBaseUrl = String.fromEnvironment('BASETEN_BASE_URL', defaultValue: 'https://inference.baseten.co/v1');
  static const reasoningModel = String.fromEnvironment('BASETEN_REASONING_MODEL', defaultValue: 'meta-llama/Llama-4-Maverick-17B-128E-Instruct');
  static const fastModel = String.fromEnvironment('BASETEN_FAST_MODEL', defaultValue: 'meta-llama/Llama-4-Scout-17B-16E-Instruct');
}
