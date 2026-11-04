import 'package:flutter/material.dart';
import '../../widgets/empty_state.dart';
import 'widgets/org_pulse_painter.dart';

class CompanyScreen extends StatefulWidget {
  const CompanyScreen({super.key});
  @override
  State<CompanyScreen> createState() => _CompanyScreenState();
}

class _CompanyScreenState extends State<CompanyScreen> with SingleTickerProviderStateMixin {
  late final AnimationController _pulseCtrl = AnimationController(vsync: this, duration: const Duration(milliseconds: 1600))..repeat();
  @override
  void dispose() { _pulseCtrl.dispose(); super.dispose(); }
  @override
  Widget build(BuildContext context) {
    return CustomScrollView(slivers: [
      const SliverAppBar.large(title: Text('Company')),
      SliverToBoxAdapter(child: Padding(padding: const EdgeInsets.all(16), child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
        Card(clipBehavior: Clip.antiAlias, child: SizedBox(height: 220, width: double.infinity, child: CustomPaint(painter: OrgPulsePainter(animation: _pulseCtrl), size: const Size(double.infinity, 220)))),
        const SizedBox(height: 12),
        Text('Charter', style: Theme.of(context).textTheme.titleMedium),
        const Card(child: ListTile(title: Text('Empower founders with an autonomous OS'), subtitle: Text('Vision: Every startup runs like Fortune 500'))),
        const SizedBox(height: 12),
        Text('OKR Progress', style: Theme.of(context).textTheme.titleMedium),
        Row(children: [Expanded(child: Card(child: Padding(padding: EdgeInsets.all(16), child: Column(children: [Text('Launch MVP'), SizedBox(height: 8), LinearProgressIndicator(value: 0.6)])))), SizedBox(width: 12), Expanded(child: Card(child: Padding(padding: EdgeInsets.all(16), child: Column(children: [Text('Hire team'), SizedBox(height: 8), LinearProgressIndicator(value: 0.3)]))))]),
        const SizedBox(height: 12),
        const EmptyState(title: 'Workforce Report', body: 'Weekly productivity + role health will appear here.'),
      ]))),
    ]);
  }
}
