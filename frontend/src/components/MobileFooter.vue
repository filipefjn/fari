<template>
    <div class="mobile-footer">
        <div class="static" @click="openModal()">
            <Seekbar class="seekbar"/>
            <div class="text">{{tracktitle}}<span class="lighter">{{artist}}</span></div>
            <fa-icon class="icon" icon="chevron-up"/>
        </div>
        <div class="modal" :class="{'display': modalOpen}">
            <div class="closebar" @click="closeModal()">
                <fa-icon class="icon" :class="{'display': modalOpen}" icon="chevron-down"/>
            </div>
            <div class="artwork-container" :style="artworkBackground">
            </div>
            <div class="song-info">
                <div class="title">{{tracktitle}}</div>
                <div class="artist">{{artistModal}}</div>
            </div>
            <!-- TODO implement seekbar -->
            <PlaybackControls class="controls" mobile/>
            <!-- TODO implement volume slider -->
        </div>
    </div>
</template>

<script>
import Seekbar from '@/components/Seekbar.vue';
import PlaybackControls from '@/components/PlaybackControls.vue';

import { mapGetters } from 'vuex';

export default {
    components: {
        Seekbar,
        PlaybackControls,
    },
    data: function() {
        return {
            modalOpen: false,
        };
    },
    computed: {
        ...mapGetters(['songInfo', 'songArtworkCounter']),
        tracktitle: function() {
            let info = this.songInfo;
            if(info && info.tags && info.tags.tracktitle) {
                return info.tags.tracktitle;
            } else {
                return ""
            }
        },
        artist: function() {
            let info = this.songInfo;
            if(info && info.tags && info.tags.artist) {
                return " - " + info.tags.artist;
            } else {
                return ""
            }
        },
        artistModal: function() {
            let info = this.songInfo;
            if(info && info.tags && info.tags.artist) {
                return info.tags.artist;
            } else {
                return ""
            }
        },
        displayArtwork: function() {
            if(this.songInfo && this.songInfo.artwork) {
                return true;
            } else {
                return false;
            }
        },
        artworkBackground: function() {
            if(this.displayArtwork) {
                return {
                    'background-image': 'url(' + this.songInfo.artwork + ')',
                }
            } else {
                return {}
            }

        }
    },
    methods: {
        openModal: function() {
            this.modalOpen = true;
        },
        closeModal: function() {
            this.modalOpen = false;
        }
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.mobile-footer {
    position: relative;

    .static {
        z-index: 1100;
        position: absolute;
        top: 0; bottom: 0; left: 0; right: 0;
        background-color: #2A2A2A;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 2rem;

        .seekbar {
            position: absolute;
            top: 0;
            left: 0;
        }

        .text {
            color: $text-color;
            margin-left: -0.5rem;
            margin-top: 0.25rem;

            .lighter {
                color: rgb(95, 95, 95);
            }
        }

        .icon {
            color: $text-color;
            font-size: 1.5rem;
        }
    }

    .modal {
        position: fixed;
        top: 0; bottom: 0; left: 0; right: 0;
        background-color: #202020;
        z-index: 2000;
        transition: transform 0.3s;
        display: flex;
        flex-direction: column;
        align-items: center;

        .expand {
            flex-grow: 1;
        }

        .closebar {
            display: flex;
            width: 100%;
            padding: 0 2rem;
            justify-content: center;
            cursor: pointer;
            align-items: center;
            height: 4rem;
            flex-shrink: 0;

            .icon {
                color: $text-color;
                font-size: 1.5rem;
                transition: opacity 0.2s;

                &:not(.display) {
                    opacity: 0;
                }

                .display {
                    opacity: 1;
                }
            }
        }

        .artwork-container {
            width: 90%;
            flex-grow: 1;
            overflow: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 1.5rem;
            background-size: contain;
            background-repeat: no-repeat;
            background-position: center center;
        }

        .song-info {

            display: flex;
            flex-direction: column;
            align-items: center;
            margin-bottom: 1.5rem;
            user-select: none;

            .title {
                color: $text-color;
                font-size: 1.25rem;
            }

            .artist {
                margin-top: 0.25rem;
                color: $text-color;
                font-size: 1rem;
                color: #888888;
            }
        }

        .controls {
            margin-bottom: 1.5rem;
        }

        &:not(.display) {
            transform: translateY(+100%);
        }

        .display {
            transform: translateY(0);
        }

    }

}
</style>
