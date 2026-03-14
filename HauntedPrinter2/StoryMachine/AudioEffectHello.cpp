#include "AudioEffectHello.h"

void AudioEffectHello::update(void)
{
    audio_block_t *in = receiveReadOnly(0);
    if (!in) return;

    audio_block_t *out = allocate();
    if (!out) {
        release(in);
        return;
    }

    // Simple "Hello World" audio effect: reduce volume to 50%
    for (int i = 0; i < AUDIO_BLOCK_SAMPLES; i++) {
        out->data[i] = in->data[i] / 2;  
    }

    transmit(out);
    release(out);
    release(in);
}
