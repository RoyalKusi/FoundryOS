import 'package:supabase_flutter/supabase_flutter.dart';
import '../config.dart';

/// Supabase wrapper with Realtime channels auto-resubscribe per CONTRACTS.
/// Channels: messages, tasks, approvals, agent_runs filtered by company_id
class SupaClient {
  static SupabaseClient get client => Supabase.instance.client;

  static Future<void> init() async {
    await Supabase.initialize(
      url: const String.fromEnvironment('SUPABASE_URL', defaultValue: 'http://localhost:54321'),
      anonKey: const String.fromEnvironment('SUPABASE_ANON_KEY', defaultValue: 'test-anon-key'),
      authOptions: const FlutterAuthClientOptions(autoRefreshToken: true),
      realtimeClientOptions: const RealtimeClientOptions(eventsPerSecond: 10),
    );
  }

  /// Subscribe to company-scoped Realtime — handles reconnect
  static RealtimeChannel subscribeCompany(String table, String companyId, void Function(Map<String, dynamic>) onInsert) {
    final channel = client.channel('public:$table:company_id=eq.$companyId');
    channel.onPostgresChanges(event: PostgresChangeEvent.insert, schema: 'public', table: table, filter: PostgresChangeFilter(type: PostgresChangeFilterType.eq, column: 'company_id', value: companyId), callback: (payload) => onInsert(payload.newRecord));
    channel.subscribe();
    return channel;
  }
}
