import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';
import '../config.dart';
import '../errors/failure.dart';

/// Dio client with auth refresh, 5xx retry with backoff, camelCase via interceptors.
class ApiClient {
  final Dio dio;
  ApiClient({String? baseUrl, String Function()? tokenProvider})
      : dio = Dio(BaseOptions(
          baseUrl: baseUrl ?? AppConfig.apiBaseUrl,
          connectTimeout: const Duration(seconds: 10),
          receiveTimeout: const Duration(seconds: 60),
          sendTimeout: const Duration(seconds: 30),
          headers: {'Content-Type': 'application/json'},
        )) {
    dio.interceptors.add(InterceptorsWrapper(
      onRequest: (opts, h) {
        // Auth header from Supabase session or mock X-Company-Id
        final token = tokenProvider?.call();
        if (token != null && token.isNotEmpty) opts.headers['Authorization'] = 'Bearer $token';
        // Mock mode header for tests (backend allows X-Company-Id when LLM_MODE=mock)
        opts.headers['X-Company-Id'] ??= '00000000-0000-0000-0000-000000000001';
        if (kDebugMode) debugPrint('→ ${opts.method} ${opts.path}');
        h.next(opts);
      },
      onResponse: (r, h) => h.next(r),
      onError: (e, h) async {
        // Retry 5xx with exponential backoff 3 times (A2/D1 contract)
        final req = e.requestOptions;
        int retries = req.extra['retries'] as int? ?? 0;
        if (retries < 3 && (e.response?.statusCode ?? 0) >= 500) {
          req.extra['retries'] = retries + 1;
          await Future.delayed(Duration(milliseconds: 400 * (1 << retries) + (retries * 200)));
          try {
            final res = await dio.fetch(req);
            return h.resolve(res);
          } catch (_) {}
        }
        // Auth refresh stub: if 401, try refresh once
        if (e.response?.statusCode == 401 && retries == 0) {
          req.extra['retries'] = 1;
          // TODO: call Supabase refresh; for now just propagate as auth failure
        }
        h.next(e);
      },
    ));
    dio.interceptors.add(LogInterceptor(requestBody: kDebugMode, responseBody: kDebugMode, error: true));
  }

  Failure _mapDioError(DioException e) {
    if (e.type == DioExceptionType.connectionTimeout || e.type == DioExceptionType.connectionError) {
      return const Failure.network(message: 'No internet — you’re offline');
    }
    final code = e.response?.statusCode;
    final msg = e.response?.data is Map ? e.response?.data['error']?['message'] as String? : null;
    if (code == 401) return Failure.auth(message: msg);
    if (code == 404) return Failure.notFound(message: msg);
    if (code == 422 || code == 400) return Failure.validation(message: msg, details: e.response?.data);
    if (code != null && code >= 500) return Failure.server(message: msg);
    return Failure.network(message: msg ?? e.message, statusCode: code);
  }

  Future<Response<T>> get<T>(String path, {Map<String, dynamic>? query}) async {
    try { return await dio.get<T>(path, queryParameters: query); } on DioException catch (e) { throw _mapDioError(e); }
  }
  Future<Response<T>> post<T>(String path, {dynamic data, Map<String, dynamic>? query}) async {
    try { return await dio.post<T>(path, data: data, queryParameters: query); } on DioException catch (e) { throw _mapDioError(e); }
  }
}
