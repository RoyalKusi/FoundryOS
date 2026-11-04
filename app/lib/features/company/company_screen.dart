import 'package:flutter/material.dart';
import '../../widgets/empty_state.dart';
import 'widgets/org_pulse_painter.dart';

class CompanyScreen extends StatelessWidget {
  const CompanyScreen({super.key});
  @override
  Widget build(BuildContext context) {
    return CustomScrollView(
      slivers: [
        const SliverAppBar.large(title: Text('Company')),
        SliverToBoxAdapter(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              children: [
                SizedBox(height: 200, child: CustomPaint(painter: OrgPulsePainter(), size: const Size(double.infinity, 200))),
                const SizedBox(height: 24),
                const EmptyState(title: 'No activity yet', body: 'Create your Charter in Genesis to see Org Pulse.'),
              ],
            ),
          ),
        ),
      ],
    );
  }
}
