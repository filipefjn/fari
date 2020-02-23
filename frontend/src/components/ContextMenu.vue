<template>
    <div class="context-menu-container"
        :class="{'show': show}"
        :style="containerStyle"
        @click="onClick($event)"
        @mouseleave="onMouseLeave($event)">
        <div class="context-menu">
            <slot></slot>
        </div>
    </div>
</template>

<script>
import ContextMenuItem from "@/components/ContextMenuItem.vue";

export default {
    props: {
        posX: Number,
        posY: Number,
        show: {
            type: Boolean,
            required: true
        }
    },
    components: {
        ContextMenuItem
    },
    computed: {
        containerStyle: function() {
            return {
                'left': this.posX + 'px',
                'top': this.posY + 'px',
            }
        }
    },
    methods: {
        onMouseLeave(event) {
            this.$emit('mouseleave', event);
        },
        onClick(event) {
            this.$emit('close');
        }
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.context-menu-container {
    z-index: 1400;
    position: fixed;
    transform: translate(calc(1rem - 100%), -1rem);
    padding: 1rem;
    opacity: 1;
    transition: opacity 0.3s;
    pointer-events: all;

    &:not(.show) {
        pointer-events: none;
        opacity: 0;
    }

    .context-menu {
        background-color: $context-menu-bgcolor;
        box-shadow: $context-menu-shadow;
        border-radius: 2px;
        padding: 0 0;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        align-items: stretch;
    }
}

</style>
