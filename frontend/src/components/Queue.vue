<template>
    <div class="container">
        <ContentList>
            <ContentListItem v-for="item in queueList" :key="item.id" @click="playQueuePosition(item.pos)">
                <div class="icon" v-if="queuePlayIndex == item.pos"><fa-icon icon="play" style="font-size: 1rem;"/></div>
                <div class="icon" v-else></div>
                {{item.name}}
            </ContentListItem>
        </ContentList>
    </div>
</template>

<script>
import ContentList from '@/components/ContentList.vue';
import ContentListItem from '@/components/ContentListItem.vue';
import { mapGetters } from 'vuex';

export default {
    components: {
        ContentList,
        ContentListItem
    },
    data: function() {
        return {
            keyCounter: 0,
        };
    },
    mounted: function() {
        this.$store.dispatch('setHeaderInfo', {
            title: "Queue",
        });
    },
    computed: {
        ...mapGetters(['queue', 'queuePlayIndex']),
        queueList: function() {
            let list = [];
            for(let i = 0; i < this.queue.length; i++) {
                // TODO improve
                list.push({
                    id: this.keyCounter,
                    pos: i,
                    name: this.queue[i].path.split("/").reverse()[0]
                });
                this.keyCounter = this.keyCounter + 1;
            }
            return list;
        }
    },
    methods: {
        playQueuePosition: function(pos) {
            this.$store.dispatch('playFromQueue', pos);
        }
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.icon {
    margin-right: 1rem;
    font-size: 1.25rem;
    width: 1rem;
    color: $list-item-icon-color;
    display: flex;
    justify-content: center;
    align-items: center;
}

</style>
