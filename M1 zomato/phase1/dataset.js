/**
 * Phase 1: Data Ingestion & Preprocessing
 * Responsible for loading the Zomato dataset from Hugging Face,
 * extracting critical fields, and indexing for fast retrieval.
 */

const DATASET_URL = 'https://datasets-server.huggingface.co/rows?dataset=ManikaSaini%2Fzomato-restaurant-recommendation&config=default&split=train&offset=0&length=500';

class DataIngestionEngine {
    constructor() {
        this.dataset = [];
        this.isLoaded = false;
    }

    /**
     * Fetches the Zomato dataset from the Hugging Face REST API.
     */
    async fetchDataset() {
        console.log("Phase 1: Starting Data Ingestion...");
        try {
            const response = await fetch(DATASET_URL);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            
            // Proceed to extraction and transformation
            this.dataset = this.extractAndClean(data.rows);
            this.isLoaded = true;
            console.log(`Phase 1 Complete: Successfully ingested and indexed ${this.dataset.length} restaurants.`);
            return this.dataset;
            
        } catch (error) {
            console.error("Phase 1 Error: Failed to ingest dataset.", error);
            // Fallback to empty array to prevent complete crash as per edge cases
            return [];
        }
    }

    /**
     * Parses and cleans critical structured fields.
     * Maps the raw API response to the required application format.
     */
    extractAndClean(rawRows) {
        const cleanedData = [];

        rawRows.forEach(item => {
            const row = item.row;

            // Missing Critical Fields Edge Case Handling
            if (!row.name || !row.location || !row.cuisines) {
                return; // Exclude entries missing vital data
            }

            // Extract and clean cost
            let cost = 0;
            if (row['approx_cost(for two people)']) {
                // Remove commas and parse to integer (e.g., "1,200" -> 1200)
                cost = parseInt(row['approx_cost(for two people)'].replace(/,/g, ''), 10);
            }
            if (isNaN(cost)) cost = 500; // Impute default if broken

            // Extract and clean rating
            let rating = 0;
            if (row.rate && row.rate !== "NEW" && row.rate !== "-") {
                // Parse "4.1/5" to 4.1
                rating = parseFloat(row.rate.split('/')[0]);
            }
            if (isNaN(rating)) rating = 3.0; // Impute default rating

            cleanedData.push({
                id: item.row_idx,
                name: row.name.trim(),
                location: row.location.trim(),
                address: row.address ? row.address.trim() : "",
                cuisines: row.cuisines.split(',').map(c => c.trim()),
                costForTwo: cost,
                rating: rating,
                votes: row.votes || 0,
                // Indexing for rapid text search
                _searchIndex: `${row.name} ${row.location} ${row.cuisines}`.toLowerCase()
            });
        });

        // Sort by rating desc as a default optimal index
        return cleanedData.sort((a, b) => b.rating - a.rating);
    }

    getDataset() {
        return this.dataset;
    }
}

// Export for usage
window.DataIngestionEngine = DataIngestionEngine;
