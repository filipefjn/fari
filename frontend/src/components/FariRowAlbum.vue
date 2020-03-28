<template>
    <div class="album-container">
        <div class="album-artwork"></div>
        <div class="album-info">
            <div class="album-title">{{title}}</div>
            <div class="album-artist"><span v-if="year">{{year}} - </span>{{artist}}</div>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        artist: {
            type: String,
            required: true,
        },
        title: {
            type: String,
            required: true,
        },
        year: {
            type: String,
        }
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.album-container {
    display: flex;
    padding: 1rem 0.5rem;
    padding-top: 2rem;
    align-items: center;

    .album-artwork {
        height: 4.5rem;
        width: 4.5rem;
        background-color: #282828;
    }

    .album-info {
        display: flex;
        flex-direction: column;
        justify-content: space-around;
        padding-left: 1rem;
        color: $text-color;

        .album-title {
            font-size: 1.25rem;
        }

        .album-artist {
            font-size: 0.9rem;
            margin-top: 0.25rem;
            color: darken($text-color, 20%);
        }
    }
}

</style>
