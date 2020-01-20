<template>
    <div class="footer-container">
        <SongInfo class="left"/>
        <PlaybackControls class="center"/>
        <div class="right"></div>
    </div>
</template>

<script>
import SongInfo from '@/components/SongInfo.vue';
import PlaybackControls from '@/components/PlaybackControls.vue';

export default {
    components: {
        SongInfo,
        PlaybackControls
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.footer-container {
    position: relative;

    .left, .center, .right {
        position: absolute;
        height: 100%;
    }

    .left {
        left: 1rem;
    }

    .center {
        left: 50%;
        transform: translateX(-50%);
    }

    .right {
        right: 1rem;
    }
}
</style>
