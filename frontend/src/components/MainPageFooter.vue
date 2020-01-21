<template>
    <div class="footer-root">
        <Seekbar class="seekbar"/>
        <div class="footer-container">
            <SongInfo class="left"/>
            <PlaybackControls class="center"/>
            <VolumeSlider class="right"/>
        </div>
    </div>
</template>

<script>
import SongInfo from '@/components/SongInfo.vue';
import PlaybackControls from '@/components/PlaybackControls.vue';
import Seekbar from '@/components/Seekbar.vue';
import VolumeSlider from '@/components/VolumeSlider.vue';

export default {
    components: {
        SongInfo,
        PlaybackControls,
        Seekbar,
        VolumeSlider
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.footer-root {

    position: relative;

    .seekbar {
        position: absolute;
        top: 0;
        left: 0;
    }

    .footer-container {

        position: absolute;
        top: 0;
        bottom: 0;
        left: 0;
        right: 0;

        .left, .center, .right {
            position: absolute;
            height: 100%;
        }

        .left {
            left: 0.75rem;
        }

        .center {
            left: 50%;
            transform: translateX(-50%);
        }

        .right {
            right: 2rem;
        }
    }
}
</style>
