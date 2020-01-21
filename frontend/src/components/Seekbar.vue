<template>
    <div class="seekbar" ref="seekbar" @click="onClick($event)">
        <div class="seekbar-background">
            <div class="progress" :style="progressStyle"></div>
        </div>
    </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
    computed: {
        ...mapGetters(['playerInfo']),
        progressStyle: function() {
            let progress = this.playerInfo.progress;
            if(!progress) {
                progress = 0;
            }
            return {
                'width': (progress * 100) + "%"
            }
        },
    },
    methods: {
        onClick: function(event) {
            let position = event.layerX / this.$refs.seekbar.offsetWidth;
            this.$store.dispatch('seekPosition', position);
        }
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.seekbar {
    height: 10px;
    width: 100%;
    padding: 0;
    margin: 0;
    overflow: hidden;
    cursor: pointer;
    z-index: 1000;
    margin-top: -2px;
    display: flex;
    align-items: center;
    transition: height 0.25s, padding 0.25;

    .seekbar-background {

        background-color: #333333;
        height: 4px;
        width: 100%;
        overflow: hidden;
        transition: height 0.25s;

        .progress {
            height: 4px;
            margin: 0;
            width: 100%;
            background-color: $primary;
            transition: width .2s linear, height 0.25s;
        }
    }

    &:hover {
        padding: 0 0;

        .seekbar-background {
            height: 8px;

            .progress {
                height: 8px;
            }
        }


    }
}
</style>
