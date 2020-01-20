<template>
    <div class="playback-controls-container">
        <button class="button"></button>
        <button class="button play"></button>
        <button class="button"></button>
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
        box-shadow: 2px 2px 2px rgba(0, 0, 0, 0.15), -2px -2px 2px rgba(255, 255, 255, 0.04);
        margin: 0 0.25rem 0 0.25rem;
        cursor: pointer;

        &.play {
            height: 2rem;
            width: 2rem;
        }
    }
}
</style>
