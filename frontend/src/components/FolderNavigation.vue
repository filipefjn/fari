<template>
    <div class="container">
        <ContentList>
            <SimpleRow v-if="currentDir !== '/'" @click="openSubfolder('..')">
                <div class="icon"><fa-icon icon="level-up-alt"/></div>
                ..
            </SimpleRow>
            <SimpleRow v-for="item in subfolders" @click="openSubfolder(item)" :key="item">
                <div class="icon"><fa-icon icon="folder"/></div>
                {{item}}
            </SimpleRow>
            <SimpleRow v-for="item in files" :key="item" @click="queueFolder(item)">
                <div class="icon"><fa-icon icon="music"/></div>
                {{item}}
            </SimpleRow>
        </ContentList>
    </div>
</template>

<script>
import ContentList from '@/components/ContentList.vue';
import SimpleRow from '@/components/SimpleRow.vue';

export default {
    components: {
        ContentList,
        SimpleRow
    },
    data: function() {
        return {
            currentDir: '/',
            subfolders: null,
            files: null,
            loading: true,
        };
    },
    mounted: function() {
        this.fetchFolderContent();
    },
    activated: function() {
        this.updateHeader();
    },
    methods: {
        fetchFolderContent: function() {
            fetch('/api/folder-content', {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    path: this.currentDir,
                })
            }).then((response) => {
                return response.json();
            }).then((response) => {
                this.subfolders = response.subfolders;
                this.files = response.files;
                this.loading = false;
            })
        },
        openSubfolder: function(path) {
            this.loading = true;
            this.subfolders = null;
            this.files = null;
            if(path == '..') {
                this.currentDir = this.currentDir.split('/').reverse().slice(2).reverse().join('/') + "/";
                if(!this.currentDir) {
                    this.currentDir = "/";
                }
            } else {
                this.currentDir = this.currentDir + path + "/";
            }
            this.fetchFolderContent();
        },
        queueFolder: async function(file) {
            let queue = [];
            let queuePlayIndex = 0;
            for(let i = 0; i < this.files.length; i++) {
                if(this.files[i] == file) {
                    queuePlayIndex = i;
                }
                queue.push({
                    path: this.currentDir + this.files[i]
                });
            }
            await this.$store.dispatch('setQueue', queue);
            await this.$store.dispatch('playFromQueue', queuePlayIndex);
        },
        updateHeader: function() {
            this.$store.dispatch('setHeaderInfo', {
                    title: "Folders",
                    subtitle: this.currentDir
                })
        }
    },
    watch: {
        currentDir: {
            handler: function(val) {
                this.updateHeader();
            },
            immediate: true
        }
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.container {

    .icon {
        margin-right: 1rem;
        font-size: 1.25rem;
        width: 1rem;
        color: $list-item-icon-color;
        display: flex;
        justify-content: center;
        align-items: center;
    }

}
</style>
