import 'dart:async';
import 'dart:convert';
import 'package:dio/dio.dart';
import '../config.dart';

/// SSE streaming for agent_runs — wraps Dio response stream, yields JSON chunks.
/// Contract: GET /api/v1/agent_runs/{id}/stream → text/event-stream
class SseClient {
  final Dio _dio;
  SseClient(this._dio);

  Stream<Map<String, dynamic>> streamRun(String runId, {String? token}) async* {
    final resp = await _dio.get<ResponseBody>(
      '/api/v1/agent_runs/$runId/stream',
      options: Options(responseType: ResponseType.stream, headers: {if (token != null) 'Authorization': 'Bearer $token'}),
    );
    final stream = resp.data!.stream.map((bytes) => utf8.decode(bytes)).transform(const LineSplitter());
    await for (final line in stream) {
      if (line.startsWith('data: ')) {
        final jsonStr = line.substring(6).trim();
        if (jsonStr.isEmpty || jsonStr == '[DONE]') break;
        yield json.decode(jsonStr) as Map<String, dynamic>;
      }
    }
  }
}

/// Mock SSE for FakeApi dev (WS-E never blocks on backend)
class FakeSseClient extends SseClient {
  FakeSseClient() : super(Dio(BaseOptions(baseUrl: AppConfig.apiBaseUrl)));
  @override
  Stream<Map<String, dynamic>> streamRun(String runId, {String? token}) async* {
    for (final chunk in ['Thinking...', 'Drafting Charter...', 'Done.']) {
      await Future.delayed(const Duration(milliseconds: 400));
      yield {'type': 'token', 'content': chunk};
    }
    yield {'type': 'done', 'runId': runId};
  }
}
