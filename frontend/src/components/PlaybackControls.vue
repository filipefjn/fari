<template>
    <div class="controls-root" :class="{'mobile': mobile}">
        <div class="playback-time">{{currentPlaybackTime}}<span class="separator">/</span>{{playbackDuration}}</div>
        <div class="controls-container">
            <button class="button" @click="playPrevious()"><fa-icon icon="backward" style="margin-right: 1px"/></button>
            <button class="button play" @click="togglePause()">
                <fa-icon v-if="playOrPauseIcon == 'play'" icon="play" style="margin-left: 2px"/>
                <fa-icon v-if="playOrPauseIcon == 'pause'" icon="pause"/>
            </button>
            <button class="button" @click="playNext()"><fa-icon icon="forward" style="margin-left: 1px"/></button>
        </div>
    </div>

</template>

<script>
import { mapGetters } from "vuex";

export default {
    props: {
        mobile: {
            type: Boolean,
            default: false
        }
    },
    computed: {
        ...mapGetters(['playerStatus', 'playerInfo']),
        playOrPauseIcon: function() {
            if(this.playerStatus == 'playing') {
                return 'pause';
            } else {
                return 'play';
            }
        },
        currentPlaybackTime: function() {
            if(this.playerInfo && this.playerInfo.currentTime) {
                return this.formatPlaybackTime(this.playerInfo.currentTime);
            } else {
                return "0:00";
            }
        },
        playbackDuration: function() {
            if(this.playerInfo && this.playerInfo.duration) {
                return this.formatPlaybackTime(this.playerInfo.duration);
            } else {
                return "0:00";
            }
        }
    },
    methods: {
        togglePause: function() {
            if(this.playerStatus == 'playing') {
                this.$store.dispatch('pausePlayer')
            } else if(this.playerStatus == 'paused') {
                this.$store.dispatch('unpausePlayer')
            }
        },
        playNext: function() {
            this.$store.dispatch('playNextFromQueue');
        },
        playPrevious: function() {
            this.$store.dispatch('playPreviousFromQueue');
        },
        formatPlaybackTime: function(val) {
            if(!val) {
                val = 0;
            }
            val = Math.floor(val);
            let minutes = Math.floor(val / 60).toFixed();
            let seconds = (val % 60).toFixed();
            if(seconds.length == 1) {
                seconds = "0" + seconds;
            }
            return minutes + ":" + seconds;
        },
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.controls-root {

    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    .playback-time {
        font-size: 0.75rem;
        margin-bottom: 0.5rem;
        color: $text-color;
        user-select: none;

        .separator {
            margin: 0 0.5rem;
        }
    }

    .controls-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 2px;

        .button {
            border-radius: 50%;
            height: 1.5rem;
            width: 1.5rem;
            border: none;
            outline: none;
            background-color: #2A2A2A;
            color: $text-color;
            box-shadow: $button-shadow;
            margin: 0 0.25rem 0 0.25rem;
            cursor: pointer;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 0.75rem;

            &:active {
                box-shadow: $button-shadow-pressed;
            }

            &.play {
                height: 2rem;
                width: 2rem;
            }
        }
    }
}

.mobile {
    .playback-time {
        font-size: 1rem;
        margin-bottom: 1rem;
    }
    .controls-container {
        .button {
            height: 2.5rem;
            width: 2.5rem;
            font-size: 1.25rem;
            margin: 0 0.5rem 0 0.5rem;
            box-shadow: none;
            &.play {
                height: 3rem;
                width: 3rem;
            }
        }
    }
}
</style>
