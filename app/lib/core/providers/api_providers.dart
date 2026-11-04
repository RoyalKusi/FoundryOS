import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../network/dio_client.dart';
import '../network/sse_client.dart';
import '../network/supabase_client.dart';
import '../cache/app_database.dart';
import '../config.dart';

/// Global DI — App never calls LLM directly; all via backend
final apiClientProvider = Provider<ApiClient>((ref) => ApiClient(baseUrl: AppConfig.apiBaseUrl));

final sseClientProvider = Provider<SseClient>((ref) => AppConfig.isMock ? FakeSseClient() : SseClient(ref.read(apiClientProvider).dio));

final supaProvider = Provider((ref) => SupaClient());

final driftProvider = Provider<AppDatabase>((ref) => appDatabase);

/// Auth state — Supabase session → JWT company_id
final authProvider = StateProvider<String?>((ref) => null);

final companyIdProvider = Provider<String?>((ref) => ref.watch(authProvider) ?? '00000000-0000-0000-0000-000000000001');
