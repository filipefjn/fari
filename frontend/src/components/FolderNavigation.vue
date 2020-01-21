<template>
    <div class="container">
        <div class="header">
            <div class="title">Folders</div>
            <div class="path">{{currentDir}}</div>
        </div>
        <div class="list">
            <div class="list-item" v-if="currentDir !== '/'" @click="openSubfolder('..')">..</div>
            <div class="list-item" v-for="item in subfolders" @click="openSubfolder(item)" :key="item">{{item}}</div>
            <div class="list-item" v-for="item in files" :key="item">{{item}}</div>
        </div>
    </div>
</template>

<script>
export default {
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
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.container {

    padding-bottom: 2rem;

    &> * {
        padding-right: 2rem;
        padding-left: 2rem;
    }

    .header {
        height: 5rem;
        display: flex;
        align-items: center;
        padding-left: 2rem;
        background-image: linear-gradient(black, rgba(0,0,0,0));

        .title {
            font-size: 2rem;
            color: $primary;
            margin-right: 2rem;
        }
        .path {
            font-size: 1rem;
            color: $primary;
            margin-top: 0.5rem;
        }
    }

    .list {

        .list-item {
            padding-top: $list-item-hor-padding;
            padding-bottom: $list-item-hor-padding;
            padding-left: 1rem;
            padding-right: 1rem;
            border-top: solid 2px $list-item-line-color;
            color: $text-color;
            cursor: pointer;

            &:last-child {
                border-bottom: solid 2px $list-item-line-color;
            }

            &:hover {
                background-color: $list-item-hover-bgcolor;
            }
        }
    }
}


</style>
