#ifndef AudioEffectHello_h_
#define AudioEffectHello_h_

#include <Arduino.h>
#include <AudioStream.h>
#include <utility/imxrt_hw.h>

class AudioEffectHello : public AudioStream {
public:
    AudioEffectHello() : AudioStream(1, inputQueueArray) {}

    virtual void update(void);

private:
    audio_block_t *inputQueueArray[1];
};

#endif
