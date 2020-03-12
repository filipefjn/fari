<template>
    <div class="container" :style="containerStyle">
        <fa-icon icon="volume-up" class="volume-icon" />
        <div class="volume">
            <input type="range" class="slider" v-model="value" @wheel="onWheel($event)"/>
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
    data: function() {
        return {
            value: 100,
        };
    },
    computed: {
        ...mapGetters(["playerVolume"]),
        containerStyle: function() {
            return {
                'width': this.width,
            }
        }
    },
    methods: {
        onWheel: function(event) {
            if(event.deltaY < 0) {
                this.value += 10;
            } else if(event.deltaY > 0) {
                this.value -= 10;
            }
        }
    },
    watch: {
        value: function(val) {
            this.$store.dispatch("setPlayerVolume", (val / 100));
        },
        playerVolume: {
            handler: function(val) {
                if((this.value / 100) !== val) {
                    this.value = (val * 100);
                }
            },
            immediate: true
        }
    }
};
</script>

<style scoped lang="scss">
@import "@/style.scss";

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

        .slider {
            background-color: white;
            height: 4px;
            border-radius: 3px;
        }
    }
}

input[type="range"] {
    height: 18px;
    -webkit-appearance: none;
    margin: 10px 0;
    width: 100%;
}
input[type="range"]:focus {
    outline: none;
}
input[type="range"]::-webkit-slider-runnable-track {
    width: 100%;
    height: 4px;
    cursor: pointer;
    animate: 0.2s;
    box-shadow: 0px 0px 0px #000000;
    background: rgb(156, 156, 156);
    border-radius: 5px;
    border: 0px solid #000000;
}
input[type="range"]::-webkit-slider-thumb {
    box-shadow: 0px 0px 0px #000000;
    border: 0px solid #000000;
    height: 12px;
    width: 12px;
    border-radius: 6px;
    background: #ffffff;
    cursor: pointer;
    -webkit-appearance: none;
    margin-top: -3px;
}
input[type="range"]:focus::-webkit-slider-runnable-track {
    background: rgb(156, 156, 156);
}
input[type="range"]::-moz-range-track {
    width: 100%;
    height: 4px;
    cursor: pointer;
    animate: 0.2s;
    box-shadow: 0px 0px 0px #000000;
    background: rgb(156, 156, 156);
    border-radius: 5px;
    border: 0px solid #000000;
}
input[type="range"]::-moz-range-thumb {
    box-shadow: 0px 0px 0px #000000;
    border: 0px solid #000000;
    height: 12px;
    width: 12px;
    border-radius: 6px;
    background: #ffffff;
    cursor: pointer;
}
input[type="range"]::-ms-track {
    width: 100%;
    height: 6px;
    cursor: pointer;
    animate: 0.2s;
    background: transparent;
    border-color: transparent;
    color: transparent;
}
input[type="range"]::-ms-fill-lower {
    background: rgb(156, 156, 156);
    border: 0px solid #000000;
    border-radius: 10px;
    box-shadow: 0px 0px 0px #000000;
}
input[type="range"]::-ms-fill-upper {
    background: rgb(156, 156, 156);
    border: 0px solid #000000;
    border-radius: 10px;
    box-shadow: 0px 0px 0px #000000;
}
input[type="range"]::-ms-thumb {
    margin-top: 1px;
    box-shadow: 0px 0px 0px #000000;
    border: 0px solid #000000;
    height: 12px;
    width: 12px;
    border-radius: 5px;
    background: #ffffff;
    cursor: pointer;
}
input[type="range"]:focus::-ms-fill-lower {
    background: rgb(156, 156, 156);
}
input[type="range"]:focus::-ms-fill-upper {
    background: rgb(156, 156, 156);
}
</style>
