import 'package:flutter/material.dart';
import '../../widgets/empty_state.dart';
import '../../widgets/approval_sheet.dart';

class InboxScreen extends StatefulWidget {
  const InboxScreen({super.key});
  @override
  State<InboxScreen> createState() => _InboxScreenState();
}

class _InboxScreenState extends State<InboxScreen> {
  final List<Map<String, String>> _items = [
    {'title': 'Send launch email', 'desc': 'To 500 waitlist — needs approval', 'impact': 'External send (gated)'},
    {'title': 'Publish pricing page', 'desc': 'Draft by Marketing Lead', 'impact': 'Publish (gated)'},
  ];

  void _handleAction(int i, bool approve) {
    final removed = _items.removeAt(i);
    setState(() {});
    ScaffoldMessenger.of(context).showSnackBar(SnackBar(
      content: Text(approve ? 'Approved: ${removed['title']}' : 'Rejected: ${removed['title']}'),
      action: SnackBarAction(label: 'Undo (5s)', onPressed: () => setState(() => _items.insert(i, removed))),
      duration: const Duration(seconds: 5),
    ));
  }

  @override
  Widget build(BuildContext context) {
    return CustomScrollView(slivers: [
      const SliverAppBar.large(title: Text('Approvals')),
      if (_items.isEmpty)
        const SliverFillRemaining(child: EmptyState(title: 'No approvals', body: 'Decisions awaiting you will show here.'))
      else
        SliverPadding(
          padding: const EdgeInsets.all(12),
          sliver: SliverList.builder(
            itemCount: _items.length,
            itemBuilder: (c, i) => Dismissible(
              key: ValueKey(_items[i]['title']),
              background: Container(color: Colors.green, alignment: Alignment.centerLeft, padding: const EdgeInsets.symmetric(horizontal: 20), child: const Icon(Icons.check_rounded, color: Colors.white)),
              secondaryBackground: Container(color: Colors.red, alignment: Alignment.centerRight, padding: const EdgeInsets.symmetric(horizontal: 20), child: const Icon(Icons.close_rounded, color: Colors.white)),
              confirmDismiss: (dir) async {
                final approve = dir == DismissDirection.startToEnd;
                _handleAction(i, approve);
                return false; // we handle removal + undo ourselves
              },
              child: Card(
                margin: const EdgeInsets.only(bottom: 12),
                child: ListTile(
                  title: Text(_items[i]['title']!),
                  subtitle: Text(_items[i]['desc']!),
                  trailing: const Icon(Icons.chevron_right_rounded),
                  onTap: () => showModalBottomSheet(context: context, builder: (_) => ApprovalSheet(approval: _items[i]), isScrollControlled: true),
                ),
              ),
            ),
          ),
        ),
    ]);
  }
}
