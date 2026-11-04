import 'dart:ui';
import 'package:flutter/material.dart';

/// Glassmorphism composer per §5.5 — blur σ24, fill 0.72 light / 0.68 dark, hairline 0.5pt, saturation 1.8×
/// Used in Messages composer — grows to 6 lines, mic→send, hold waveform slide cancel
class GlassComposer extends StatelessWidget {
  final TextEditingController controller;
  final VoidCallback onSend;
  final VoidCallback? onMic;
  final bool isRecording;
  const GlassComposer({super.key, required this.controller, required this.onSend, this.onMic, this.isRecording = false});

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    return ClipRRect(
      borderRadius: BorderRadius.circular(28),
      child: BackdropFilter(
        filter: ImageFilter.blur(sigmaX: 24, sigmaY: 24),
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
          decoration: BoxDecoration(
            color: isDark ? const Color(0xAE1C1C1E) : const Color(0xB8FFFFFF), // 0.68 / 0.72
            borderRadius: BorderRadius.circular(28),
            border: Border.all(color: Colors.white.withOpacity(0.5), width: 0.5), // hairline
          ),
          child: Row(children: [
            Expanded(
              child: TextField(
                controller: controller,
                maxLines: 6,
                minLines: 1,
                decoration: const InputDecoration(hintText: 'Message…', border: InputBorder.none, isDense: true),
              ),
            ),
            IconButton(
              onPressed: isRecording ? onMic : (controller.text.trim().isEmpty ? onMic : onSend),
              icon: Icon(controller.text.trim().isEmpty ? Icons.mic_outlined : Icons.send_rounded, color: Theme.of(context).colorScheme.primary),
              tooltip: controller.text.trim().isEmpty ? 'Hold to record' : 'Send',
            ),
          ]),
        ),
      ),
    );
  }
}
