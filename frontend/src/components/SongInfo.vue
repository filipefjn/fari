<template>
    <div class="song-info-container">
        <div class="title">Track title</div>
        <div class="artist">Artist</div>
    </div>
</template>

<script>
export default {

}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.song-info-container {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    justify-content: center;

    .title {
        color: $text-color;
    }

    .artist {
        margin-top: 0.25rem;
        color: $text-color;
        font-size: 0.75rem;
    }
}
</style>
