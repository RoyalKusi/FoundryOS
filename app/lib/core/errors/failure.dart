import 'package:freezed_annotation/freezed_annotation.dart';

part 'failure.freezed.dart';

@freezed
sealed class Failure with _$Failure {
  const factory Failure.network({String? message, int? statusCode}) = NetworkFailure;
  const factory Failure.auth({String? message}) = AuthFailure;
  const factory Failure.notFound({String? message}) = NotFoundFailure;
  const factory Failure.validation({String? message, Map<String, dynamic>? details}) = ValidationFailure;
  const factory Failure.server({String? message}) = ServerFailure;
  const factory Failure.cache({String? message}) = CacheFailure;
  const factory Failure.unknown({String? message}) = UnknownFailure;

  const Failure._();

  String get displayMessage => when(
        network: (m, c) => m ?? 'Network error — check connection',
        auth: (m) => m ?? 'Session expired — sign in again',
        notFound: (m) => m ?? 'Not found',
        validation: (m, _) => m ?? 'Check your input',
        server: (m) => m ?? 'Something went wrong — try again',
        cache: (m) => m ?? 'Offline data unavailable',
        unknown: (m) => m ?? 'Unknown error',
      );
}
