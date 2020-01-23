<template>
    <div class="mobile-footer">
        <div class="static" @click="openModal()">
            <Seekbar class="seekbar"/>
            <div class="text">{{tracktitle}}<span class="lighter">{{artist}}</span></div>
            <fa-icon class="icon" icon="chevron-up"/>
        </div>
        <div class="modal" :class="{'display': modalOpen}" @click="closeModal()">
            <!-- TODO implement! -->
        </div>
    </div>
</template>

<script>
import Seekbar from '@/components/Seekbar.vue';

import { mapGetters } from 'vuex';

export default {
    components: {
        Seekbar
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
        background-color: #242424;
        z-index: 2000;
        transition: transform 0.3s;

        &:not(.display) {
            transform: translateY(+100%);
        }

        .display {
            transform: translateY(0);
        }

    }

}
</style>
