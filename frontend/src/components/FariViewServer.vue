<template>
    <FariList>
        <div class="view-wrapper">
            <FariButton @click="onUpdateLibraryClick()">Update Library</FariButton>
            <FariButton @click="onRemakeLibraryClick()">Remake library</FariButton>
            <FariButton @click="onDeleteLibraryClick()">Delete library</FariButton>
        </div>
    </FariList>
</template>

<script>
import FariList from "@/components/FariList.vue";
import FariButton from "@/components/FariButton.vue";
import { mapGetters, mapActions } from 'vuex';

export default {
    components: {
        FariList,
        FariButton
    },
    data: function() {
        return {
            keyCounter: 0,
        };
    },
    activated: function() {
        this.setDisplayNavigationButtons(false);
        this.$store.dispatch('setHeaderInfo', {
            title: "Server",
        });
    },
    computed: {
        ...mapGetters([]),
    },
    methods: {
        ...mapActions(["setLoadingScreen", 'setDisplayNavigationButtons']),
        onRemakeLibraryClick: function() {
            fetch('/api/v2/library/remake', {
                method: 'POST'
            }).then(async (response) => {
                if(response.status === 200) {
                    window.location.reload();
                } else {
                    console.error(response);
                }
            });
            this.setLoadingScreen(true);
        },
        onUpdateLibraryClick: function() {
            fetch('/api/v2/library/update', {
                method: 'POST'
            }).then(async (response) => {
                if(response.status === 200) {
                    window.location.reload();
                } else {
                    console.error(response);
                }
            });
            this.setLoadingScreen(true);
        },
        onDeleteLibraryClick: function() {
            fetch('/api/v2/library/delete', {
                method: 'POST'
            }).then(async (response) => {
                if(response.status === 200) {
                    window.location.reload();
                } else {
                    console.error(response);
                }
            });
            this.setLoadingScreen(true);
        }
    }
}
</script>

<style scoped lang="scss">
@import '@/style.scss';

.view-wrapper {
    color: $text-color;

    @include breakpoint(mobile) {
        display: flex;
        flex-direction: column;
    }

    @include breakpoint(not-mobile) {
        display: grid;
        grid-template-columns: 50% 50%;
    }
}

</style>
