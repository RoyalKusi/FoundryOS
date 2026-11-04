import 'package:flutter/material.dart';
import '../../widgets/empty_state.dart';
class InboxScreen extends StatelessWidget {
  const InboxScreen({super.key});
  @override
  Widget build(BuildContext context) {
    return CustomScrollView(slivers: [
      const SliverAppBar.large(title: Text('Approvals')),
      SliverFillRemaining(child: EmptyState(title: 'No approvals', body: 'Decisions awaiting you will show here.')),
    ]);
  }
}
