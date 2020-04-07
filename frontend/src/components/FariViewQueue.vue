<template>
    <div class="container">
        <FariList>
            <div v-for="(song, index) in queue" :key="song.path">
                <FariRowSongId v-if="song.id" :songId="song.id" @click="playQueuePosition(index)" :noSiblings="index !== queue.length-1">
                    <template v-slot:left>
                        <!-- <div class="icon" v-if="queuePlaySongId == song.id"><fa-icon icon="play"/></div> -->
                        <!-- <div class="icon" v-else></div> -->
                    </template>
                </FariRowSongId>
                <FariRowSimple v-else @click="playQueuePosition(index)" :noSiblings="index !== queue.length-1" :selected="queuePlayIndex === index">
                    <!-- <div class="icon" v-if="queuePlayIndex === index"><fa-icon icon="play" style="font-size: 1rem;"/></div> -->
                    <!-- <div class="icon" v-else></div> -->
                    {{getNameFromPath(song.path)}}
                </FariRowSimple>
            </div>

        </FariList>
    </div>
</template>

<script>
import FariList from '@/components/FariList.vue';
import FariRowSimple from '@/components/FariRowSimple.vue';
import FariRowSongId from '@/components/FariRowSongId.vue';
import { mapGetters, mapActions } from 'vuex';

export default {
    components: {
        FariList,
        FariRowSimple,
        FariRowSongId
    },
    data: function() {
        return {
            keyCounter: 0,
        };
    },
    activated: function() {
        this.setDisplayNavigationButtons(false);
        this.$store.dispatch('setHeaderInfo', {
            title: "Queue",
        });
    },
    computed: {
        ...mapGetters(['queue', 'queuePlayIndex', 'queuePlaySongId']),
    },
    methods: {
        ...mapActions(['setDisplayNavigationButtons']),
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
