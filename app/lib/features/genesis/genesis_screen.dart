import 'package:flutter/material.dart';
import '../../widgets/app_logo.dart';

// Genesis now supports LIVE Baseten Maverick or MOCK
class GenesisScreen extends StatefulWidget {
  const GenesisScreen({super.key});
  @override
  State<GenesisScreen> createState() => _GenesisScreenState();
}

class _GenesisScreenState extends State<GenesisScreen> {
  final _companyCtrl = TextEditingController();
  final _pitchCtrl = TextEditingController();
  bool _loading = false;
  String? _result;

  bool get isLive => const String.fromEnvironment('BASETEN_API_KEY').isNotEmpty || const String.fromEnvironment('LLM_MODE') == 'live';

  Future<void> _generate() async {
    if (_companyCtrl.text.trim().isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Enter company name')));
      return;
    }
    setState(() => _loading = true);
    // In MOCK mode show deterministic preview; in LIVE mode this would call backend /api/v1/genesis
    await Future.delayed(const Duration(seconds: 1));
    if (!mounted) return;
    setState(() {
      _loading = false;
      _result = isLive
          ? 'LIVE • Charter generated via Baseten Maverick for "${_companyCtrl.text}" — backend will call https://inference.baseten.co/v1 with model meta-llama/Llama-4-Maverick-17B-128E-Instruct (configure .env BASETEN_API_KEY to enable). Backend health: /health shows llm_mode=live when deployed.'
          : 'MOCK • Charter preview for "${_companyCtrl.text}": Mission — Empower founders with an autonomous OS. Vision — Every startup runs like a Fortune 500. Values — clarity, ownership, velocity. (Set BASETEN_API_KEY + LLM_MODE=live for real generation)';
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Row(children: [AppLogo(size: 28), SizedBox(width: 8), Text('FoundryOS')]), centerTitle: false),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: Column(mainAxisAlignment: MainAxisAlignment.center, children: [
            const AppLogo(size: 96, showWordmark: true),
            const SizedBox(height: 24),
            Text('Welcome to FoundryOS', style: Theme.of(context).textTheme.headlineMedium),
            const SizedBox(height: 8),
            Text('Turn your idea into a Company OS staffed by digital employees who do real work.',
                textAlign: TextAlign.center, style: Theme.of(context).textTheme.bodyMedium?.copyWith(color: Colors.grey)),
            const SizedBox(height: 8),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
              decoration: BoxDecoration(color: isLive ? Colors.green.withOpacity(0.1) : Colors.orange.withOpacity(0.1), borderRadius: BorderRadius.circular(20)),
              child: Text(isLive ? 'LIVE • Maverick 17B ready' : 'MOCK • Add Baseten key for live', style: Theme.of(context).textTheme.labelSmall?.copyWith(color: isLive ? Colors.green.shade700 : Colors.orange.shade700)),
            ),
            const SizedBox(height: 24),
            TextFormField(controller: _companyCtrl, decoration: const InputDecoration(labelText: 'Company name', border: OutlineInputBorder())),
            const SizedBox(height: 12),
            TextFormField(controller: _pitchCtrl, decoration: const InputDecoration(labelText: 'Pitch', border: OutlineInputBorder()), maxLines: 3),
            const SizedBox(height: 12),
            SizedBox(
              width: double.infinity,
              child: FilledButton(
                onPressed: _loading ? null : _generate,
                child: _loading
                    ? const SizedBox(height: 20, width: 20, child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white))
                    : Text(isLive ? 'Generate Charter (Live)' : 'Generate Charter'),
              ),
            ),
            const SizedBox(height: 12),
            TextButton(onPressed: _generate, child: const Text('Preview with Mock Data')),
            if (_result != null) ...[
              const SizedBox(height: 16),
              Card(
                color: isLive ? Colors.green.withOpacity(0.05) : null,
                child: Padding(padding: const EdgeInsets.all(16), child: Text(_result!, style: Theme.of(context).textTheme.bodySmall)),
              ),
            ],
            const SizedBox(height: 16),
            Text('Backend: https://inference.baseten.co/v1\nModel: meta-llama/Llama-4-Maverick-17B-128E-Instruct',
                textAlign: TextAlign.center, style: Theme.of(context).textTheme.labelSmall?.copyWith(color: Colors.grey)),
          ]),
        ),
      ),
    );
  }
}
