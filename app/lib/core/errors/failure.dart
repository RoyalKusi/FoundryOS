// Production Failure — sealed, no codegen required (freezed would need build_runner)
// A2/D2 squad: Result<T,Failure> + displayMessage per §6
sealed class Failure {
  const Failure();
  String get displayMessage => switch (this) {
        NetworkFailure(:final message) => message ?? 'Network error — check connection',
        AuthFailure(:final message) => message ?? 'Session expired — sign in again',
        NotFoundFailure(:final message) => message ?? 'Not found',
        ValidationFailure(:final message) => message ?? 'Check your input',
        ServerFailure(:final message) => message ?? 'Something went wrong — try again',
        CacheFailure(:final message) => message ?? 'Offline data unavailable',
        UnknownFailure(:final message) => message ?? 'Unknown error',
      };
}

class NetworkFailure extends Failure {
  final String? message;
  final int? statusCode;
  const NetworkFailure({this.message, this.statusCode});
}
class AuthFailure extends Failure {
  final String? message;
  const AuthFailure({this.message});
}
class NotFoundFailure extends Failure {
  final String? message;
  const NotFoundFailure({this.message});
}
class ValidationFailure extends Failure {
  final String? message;
  final Map<String, dynamic>? details;
  const ValidationFailure({this.message, this.details});
}
class ServerFailure extends Failure {
  final String? message;
  const ServerFailure({this.message});
}
class CacheFailure extends Failure {
  final String? message;
  const CacheFailure({this.message});
}
class UnknownFailure extends Failure {
  final String? message;
  const UnknownFailure({this.message});
}
