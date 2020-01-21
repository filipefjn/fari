<template>
    <div class="song-info-container">
        <div class="title">{{tracktitle}}</div>
        <div class="artist">{{artist}}</div>
    </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
    computed: {
        ...mapGetters(['songInfo']),
        tracktitle: function() {
            let info = this.songInfo;
            if(info && info.tags && info.tags.tracktitle) {
                return info.tags.tracktitle;
            } else {
                return "-"
            }
        },
        artist: function() {
            let info = this.songInfo;
            if(info && info.tags && info.tags.artist) {
                return info.tags.artist;
            } else {
                return "-"
            }
        }
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.song-info-container {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: center;
    user-select: none;

    .title {
        color: $text-color;
    }

    .artist {
        margin-top: 0.25rem;
        color: $text-color;
        font-size: 0.75rem;
    }
}
</style>
