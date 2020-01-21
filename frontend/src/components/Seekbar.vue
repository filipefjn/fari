<template>
    <div class="seekbar">
        <div class="progress" :style="progressStyle"></div>
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
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.seekbar {
    height: 4px;
    width: 100%;
    background-color: #333333;
    padding: 0;
    margin: 0;
    position: relative;
    overflow: hidden;

    .progress {
        height: 4px;
        margin: 0;
        position: absolute;
        left: 0;
        background-color: $primary;
        transition: width .2s linear;
    }
}
</style>
