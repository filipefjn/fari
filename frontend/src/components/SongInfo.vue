<template>
    <div class="song-info-container">
        <div class="song-info-artwork" :class="{'outset': displayArtwork}">
            <transition name="artwork-transition" v-enter v-leave>
                <img class="artwork" v-if="displayArtwork" :key="songArtworkCounter" :src="songInfo.artwork">
            </transition>
        </div>
        <div class="song-info-text">
            <div class="title">{{tracktitle}}</div>
            <div class="artist">{{artist}}</div>
        </div>
    </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
    computed: {
        ...mapGetters(['songInfo', 'songArtworkCounter']),
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
        },
        displayArtwork: function() {
            if(this.songInfo && this.songInfo.artwork) {
                return true;
            } else {
                return false;
            }
        }
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.song-info-container {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    user-select: none;

    .song-info-artwork {
        width: 3.5rem;
        height: 3.5rem;
        padding: 0;
        box-shadow: $button-shadow-pressed;
        margin-right: 1rem;
        border-radius: 4px;
        padding: 0;
        overflow: hidden;

        &.outset {
            box-shadow: $button-shadow;
        }

        .artwork {
            width: 3.5rem;
            height: 3.5rem;
        }
    }

    .song-info-text {

        display: flex;
        flex-direction: column;
        align-items: flex-start;
        justify-content: flex-start;

        .title {
            color: $text-color;
        }

        .artist {
            margin-top: 0.25rem;
            color: $text-color;
            font-size: 0.75rem;
        }
    }

}

.artwork-transition-enter-active, .artwork-transition-leave-active {
    transition: opacity .3s;
}

.artwork-transition-enter, .artwork-transition-leave-to {
    opacity: 0;
}
</style>
