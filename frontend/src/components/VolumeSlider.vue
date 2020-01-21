<template>
    <div class="container" :style="containerStyle">
        <!-- <img src="@/assets/volume.svg" class="volume-icon"> -->
        <fa-icon icon="volume-up" class="volume-icon"/>
        <div class="volume" @click="onClick($event)">
            <div class="slider" :style="sliderStyle"></div>
        </div>
    </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
    props: {
        width: {
            type: Number,
            default: 160
        }
    },
    computed: {
        ...mapGetters(["playerVolume"]),
        containerStyle: function() {
            return {
                'width': this.width,
            }
        },
        sliderStyle: function() {
            let volume = this.playerVolume;
            if(volume === undefined || volume === null) {
                volume = 1;
            }
            return {
                'width': (volume * 100) + "%"
            }
        }
    },
    methods: {
        onClick: function(event) {
            let volume = event.layerX - 5;
            let max = this.width - 10;
            if(volume > max) {
                volume = max;
            } else if(volume < 0) {
                volume = 0;
            }
            volume = volume / max;
            this.$store.dispatch('setPlayerVolume', volume);
        }
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.container {

    position: relative;
    padding: 0;
    width: 160px;

    .volume-icon {
        position: absolute;
        top: 50%;
        left: -6px;
        height: 12px;
        transform: translate(-100%, -50%);
        color: white;
    }

    .volume {
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        width: 100%;
        height: 14px;
        border-radius: 7px;
        padding: 0 5px 0 5px;
        box-shadow: $button-shadow-pressed;
        display: flex;
        align-items: center;
        cursor: pointer;

        .slider {
            background-color: white;
            height: 4px;
            border-radius: 3px;
        }
    }
}


</style>
