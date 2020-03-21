<template>
    <div class="container">
        <ContentList>
            <div v-for="(song, index) in queue" :key="song.path">
                <SongRow v-if="song.id" :songId="song.id" @click="playQueuePosition(index)" :noSiblings="index !== queue.length-1">
                    <template v-slot:left>
                        <div class="icon" v-if="queuePlaySongId == song.id"><fa-icon icon="play"/></div>
                        <div class="icon" v-else></div>
                    </template>
                </SongRow>
                <SimpleRow v-else @click="playQueuePosition(index)" :noSiblings="index !== queue.length-1" :selected="queuePlayIndex === index">
                    <div class="icon" v-if="queuePlayIndex === index"><fa-icon icon="play" style="font-size: 1rem;"/></div>
                    <div class="icon" v-else></div>
                    {{getNameFromPath(song.path)}}
                </SimpleRow>
            </div>

        </ContentList>
    </div>
</template>

<script>
import ContentList from '@/components/ContentList.vue';
import SimpleRow from '@/components/SimpleRow.vue';
import SongRow from '@/components/SongRow.vue';
import { mapGetters } from 'vuex';

export default {
    components: {
        ContentList,
        SimpleRow,
        SongRow
    },
    data: function() {
        return {
            keyCounter: 0,
        };
    },
    activated: function() {
        this.$store.dispatch('setHeaderInfo', {
            title: "Queue",
        });
    },
    computed: {
        ...mapGetters(['queue', 'queuePlayIndex', 'queuePlaySongId']),
    },
    methods: {
        playQueuePosition: function(pos) {
            this.$store.dispatch('playFromQueue', pos);
        },
        getNameFromPath: function(path) {
            return path.split("/").slice(-1)[0];
        }
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.icon {
    margin-right: 1rem;
    font-size: 1rem;
    width: 1rem;
    color: $list-item-icon-color;
    display: flex;
    justify-content: center;
    align-items: center;
}

</style>
