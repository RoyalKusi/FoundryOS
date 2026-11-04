import 'package:flutter/material.dart';
import '../../core/widgets/glass_composer.dart';
import '../../core/widgets/shimmer.dart';
import '../../widgets/citation_chip.dart';

class ThreadListScreen extends StatefulWidget {
  const ThreadListScreen({super.key});
  @override
  State<ThreadListScreen> createState() => _T();
}

class _T extends State<ThreadListScreen> {
  final _ctrl = TextEditingController();
  final _messages = <Map<String, dynamic>>[
    {'role': 'assistant', 'kind': 'system', 'body': 'Founder’s Assistant — ask anything', 'pinned': true},
    {'role': 'ai', 'kind': 'report', 'body': 'Q1 OKR Review — 3 objectives, 60% on track', 'citations': ['charter.md', 'kpi_01']},
    {'role': 'human', 'kind': 'text', 'body': 'Can you draft the launch email?'},
  ];
  bool _streaming = false;

  void _send() {
    if (_ctrl.text.trim().isEmpty) return;
    setState(() { _messages.add({'role': 'human', 'kind': 'text', 'body': _ctrl.text}); _ctrl.clear(); _streaming = true; });
    Future.delayed(const Duration(milliseconds: 1200), () => setState(() { _messages.add({'role': 'ai', 'kind': 'text', 'body': 'Drafted — needs approval before sending (gated).'}); _streaming = false; }));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: CustomScrollView(slivers: [
        const SliverAppBar.large(title: Text('Chats')),
        SliverPadding(padding: const EdgeInsets.all(12), sliver: SliverList.builder(itemCount: _messages.length, itemBuilder: (c, i) {
          final m = _messages[i];
          final isMe = m['role'] == 'human';
          final isReport = m['kind'] == 'report';
          return MessageBubble(
            child: Align(
              alignment: isMe ? Alignment.centerRight : Alignment.centerLeft,
              child: Container(
                margin: const EdgeInsets.only(bottom: 8),
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: isMe ? Theme.of(context).colorScheme.primary : isReport ? const Color(0x195E5CE6) : Theme.of(context).colorScheme.surfaceContainerHighest,
                  borderRadius: BorderRadius.circular(14),
                ),
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text(m['body'] as String, style: TextStyle(color: isMe ? Colors.white : null)),
                  if (m['citations'] != null) ...[(const SizedBox(height: 6)), Wrap(spacing: 6, children: (m['citations'] as List).map((e) => CitationChip(label: e as String)).toList())],
                ]),
              ),
            ),
          );
        })),
        if (_streaming) const SliverToBoxAdapter(child: Padding(padding: EdgeInsets.all(12), child: StreamingShimmer())),
      ]),
      bottomNavigationBar: Padding(
        padding: EdgeInsets.only(bottom: MediaQuery.of(context).viewInsets.bottom + 8, left: 12, right: 12, top: 8),
        child: GlassComposer(controller: _ctrl, onSend: _send, onMic: () => ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Hold to record — AAC 16kHz → Whisper')))),
      ),
    );
  }
}
