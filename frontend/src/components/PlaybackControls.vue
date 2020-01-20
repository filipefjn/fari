<template>
    <div class="playback-controls-container">
        <button class="button"><fa-icon icon="backward" style="margin-right: 1px"/></button>
        <button class="button play"><fa-icon icon="play" style="margin-left: 2px"/></button>
        <button class="button"><fa-icon icon="forward" style="margin-left: 1px"/></button>
    </div>
</template>

<script>
export default {

}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.playback-controls-container {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .button {
        border-radius: 50%;
        height: 1.5rem;
        width: 1.5rem;
        border: none;
        outline: none;
        background-color: #2A2A2A;
        color: $text-color;
        box-shadow: 2px 2px 2px rgba(0, 0, 0, 0.15), -2px -2px 2px rgba(255, 255, 255, 0.04);
        margin: 0 0.25rem 0 0.25rem;
        cursor: pointer;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 0.75rem;

        &:active {
            box-shadow: inset 2px 2px 2px rgba(0, 0, 0, 0.15), inset -2px -2px 2px rgba(255, 255, 255, 0.04);
        }

        &.play {
            height: 2rem;
            width: 2rem;
        }
    }
}
</style>
