class MapDataService{

    constructor(){

        this.cache=new Map();

    }

    async request(url){

        const response=await fetch(url);

        return await response.json();

    }

    async get(url){

        if(this.cache.has(url)){

            return this.cache.get(url);

        }

        const data=await this.request(url);

        this.cache.set(url,data);

        return data;

    }

    clear(url){

        this.cache.delete(url);

    }

    clearAll(){

        this.cache.clear();

    }

}

window.mapDataService=new MapDataService();