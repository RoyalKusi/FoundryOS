import 'failure.dart';

sealed class Result<T> {
  const Result();
  factory Result.ok(T data) = Ok<T>;
  factory Result.err(Failure failure) = Err<T>;

  R fold<R>({required R Function(T data) ok, required R Function(Failure f) err}) {
    return switch (this) { Ok(:final value) => ok(value), Err(:final error) => err(error) };
  }

  bool get isOk => this is Ok<T>;
  bool get isErr => this is Err<T>;
}

class Ok<T> extends Result<T> {
  final T value;
  const Ok(this.value);
}

class Err<T> extends Result<T> {
  final Failure error;
  const Err(this.error);
}
