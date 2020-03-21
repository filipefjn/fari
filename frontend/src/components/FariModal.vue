<template>
  <div class="overlay" :class="{'show': show}" @click.self="$emit('close')">
    <div class="modal-box">
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
    props: {
        show: {
            type: Boolean,
            default: true
        }
    }
}
</script>

<style scoped lang="scss">
@import "@/style.scss";

.overlay {
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: rgba(0, 0, 0, 0.7);
    z-index: 3000;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    user-select: none;
    padding: 4rem;

    @include breakpoint(mobile) {
        padding: 2rem;
    }

    &:not(.show) {
        display: none;
    }

    .modal-box {
        min-height: 10rem;
        max-height: calc(100% - 1rem);
        // min-width: 4rem;
        // max-width: calc(100% - 1rem);
        width: 100%;
        background-color: $footer-bgcolor;
        color: $text-color;
        padding: 1rem;
        border-radius: 6px;
        cursor: initial;
    }
}
</style>
