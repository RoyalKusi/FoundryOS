// Drift offline cache stub — provides optimistic interfaces for threads/messages/tasks/approvals per pubspec drift dep.
// Full drift implementation in ws-b: tables with company_id, sync queue. This stub unblocks D1 agent + analysis.
import 'package:flutter/foundation.dart';

/// Minimal drift-like interface — real drift in `ws-b` will replace with `AppDatabase`
class AppDatabase {
  // In-memory queues for optimistic send (mirrors MASTER_PROMPT §6.2)
  final List<Map<String, dynamic>> _pendingMessages = [];
  final List<Map<String, dynamic>> _threads = [];
  final List<Map<String, dynamic>> _tasks = [];

  Future<void> cacheThreads(List<Map<String, dynamic>> items) async {
    _threads..clear()..addAll(items);
    if (kDebugMode) debugPrint('drift: cached ${items.length} threads');
  }

  Future<List<Map<String, dynamic>>> getCachedThreads() async => List.unmodifiable(_threads);

  Future<void> enqueueMessage(Map<String, dynamic> msg) async {
    _pendingMessages.add(msg);
    if (kDebugMode) debugPrint('drift: enqueued message ${msg['id']}');
  }

  Future<List<Map<String, dynamic>>> getPendingMessages() async => List.unmodifiable(_pendingMessages);

  Future<void> clearPending(String id) async => _pendingMessages.removeWhere((m) => m['id'] == id);
}

/// Singleton for DI
final appDatabase = AppDatabase();
