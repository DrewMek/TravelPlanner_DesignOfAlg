#include <algorithm>
#include <chrono>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <string>
#include <utility>
#include <vector>

using namespace std;
using Trip = pair<int, double>;
using Clock = chrono::high_resolution_clock;

static constexpr int BUDGET = 5000;
static constexpr int TRIALS = 20;

vector<Trip> parse_line(const string& line) {
    vector<Trip> result;
    size_t i = 0;
    while (i < line.size()) {
        if (line[i] == '(') {
            ++i;
            while (i < line.size() && isspace((unsigned char)line[i])) ++i;

            int city = 0;
            bool neg = false;
            if (line[i] == '-') {
                neg = true;
                ++i;
            }
            while (i < line.size() && isdigit((unsigned char)line[i])) {
                city = city * 10 + (line[i] - '0');
                ++i;
            }
            if (neg) city = -city;

            while (i < line.size() && (isspace((unsigned char)line[i]) || line[i] == ',')) ++i;

            size_t start = i;
            while (i < line.size() && line[i] != ')') ++i;
            double cost = stod(line.substr(start, i - start));

            result.push_back({city, cost});
        }
        ++i;
    }
    return result;
}

bool is_sorted_by_cost(const vector<Trip>& arr) {
    for (size_t i = 1; i < arr.size(); ++i) {
        if (arr[i - 1].second > arr[i].second) return false;
    }
    return true;
}

void write_sorted_line(ofstream& out, const vector<Trip>& arr) {
    out << "[";
    for (size_t i = 0; i < arr.size(); ++i) {
        out << "(" << arr[i].first << ", " << fixed << setprecision(2) << arr[i].second << ")";
        if (i + 1 < arr.size()) out << ", ";
    }
    out << "]\n";
}

vector<Trip> merge_two(const vector<Trip>& left, const vector<Trip>& right) {
    vector<Trip> result;
    result.reserve(left.size() + right.size());

    size_t i = 0, j = 0;
    while (i < left.size() && j < right.size()) {
        if (left[i].second <= right[j].second) {
            result.push_back(left[i++]);
        } else {
            result.push_back(right[j++]);
        }
    }
    while (i < left.size()) result.push_back(left[i++]);
    while (j < right.size()) result.push_back(right[j++]);
    return result;
}

vector<Trip> merge_sort(const vector<Trip>& arr) {
    if (arr.size() <= 1) return arr;
    size_t mid = arr.size() / 2;
    vector<Trip> left(arr.begin(), arr.begin() + mid);
    vector<Trip> right(arr.begin() + mid, arr.end());
    left = merge_sort(left);
    right = merge_sort(right);
    return merge_two(left, right);
}

int partition_lomuto(vector<Trip>& arr, int low, int high) {
    int mid = low + (high - low) / 2;
    swap(arr[mid], arr[high]);
    double pivot = arr[high].second;

    int i = low - 1;
    for (int j = low; j < high; ++j) {
        if (arr[j].second < pivot) {
            ++i;
            swap(arr[i], arr[j]);
        }
    }
    swap(arr[i + 1], arr[high]);
    return i + 1;
}

void quick_sort_lomuto_helper(vector<Trip>& arr, int low, int high) {
    if (low < high) {
        int p = partition_lomuto(arr, low, high);
        quick_sort_lomuto_helper(arr, low, p - 1);
        quick_sort_lomuto_helper(arr, p + 1, high);
    }
}

vector<Trip> quick_sort_lomuto(vector<Trip> arr) {
    if (!arr.empty()) quick_sort_lomuto_helper(arr, 0, (int)arr.size() - 1);
    return arr;
}

int partition_hoare(vector<Trip>& arr, int low, int high) {
    double pivot = arr[low + (high - low) / 2].second;
    int i = low - 1;
    int j = high + 1;

    while (true) {
        do { ++i; } while (arr[i].second < pivot);
        do { --j; } while (arr[j].second > pivot);

        if (i >= j) return j;
        swap(arr[i], arr[j]);
    }
}

void quick_sort_hoare_helper(vector<Trip>& arr, int low, int high) {
    if (low < high) {
        int p = partition_hoare(arr, low, high);
        quick_sort_hoare_helper(arr, low, p);
        quick_sort_hoare_helper(arr, p + 1, high);
    }
}

vector<Trip> quick_sort_hoare(vector<Trip> arr) {
    if (!arr.empty()) quick_sort_hoare_helper(arr, 0, (int)arr.size() - 1);
    return arr;
}

int count_trips_under_budget(const vector<Trip>& sorted_arr, int budget) {
    double total = 0.0;
    int count = 0;
    for (const auto& [city, cost] : sorted_arr) {
        if (total + cost <= budget) {
            total += cost;
            ++count;
        } else {
            break;
        }
    }
    return count;
}

template <typename SortFunc>
long long benchmark_sort(const vector<Trip>& input, SortFunc sorter, vector<Trip>* sorted_output = nullptr) {
    long long total_ns = 0;
    vector<Trip> last_result;

    for (int t = 0; t < TRIALS; ++t) {
        auto start = Clock::now();
        vector<Trip> result = sorter(input);
        auto end = Clock::now();

        total_ns += chrono::duration_cast<chrono::nanoseconds>(end - start).count();

        if (t == TRIALS - 1) last_result = std::move(result);
    }

    if (sorted_output) *sorted_output = std::move(last_result);
    return total_ns / TRIALS;
}

int main() {
    ifstream infile("roundtrip_costs.txt");
    if (!infile) {
        cerr << "Could not open roundtrip_costs.txt\n";
        return 1;
    }

    ofstream mer_out("costs_MerSort.txt");
    ofstream lom_out("costs_QSortLom.txt");
    ofstream hoa_out("costs_QSortHoa.txt");
    ofstream trip_out("trip_nums.txt");
    ofstream run_out("runtimes.txt");

    if (!mer_out || !lom_out || !hoa_out || !trip_out || !run_out) {
        cerr << "Could not open output files\n";
        return 1;
    }

    string line;
    int line_num = 0;

    while (getline(infile, line)) {
        if (line.empty()) continue;
        ++line_num;

        vector<Trip> city_list = parse_line(line);

        vector<Trip> mer_sorted, lom_sorted, hoa_sorted;

        long long mer_time = benchmark_sort(city_list, merge_sort, &mer_sorted);
        long long lom_time = benchmark_sort(city_list, quick_sort_lomuto, &lom_sorted);
        long long hoa_time = benchmark_sort(city_list, quick_sort_hoare, &hoa_sorted);

        if (!is_sorted_by_cost(mer_sorted) || !is_sorted_by_cost(lom_sorted) || !is_sorted_by_cost(hoa_sorted)) {
            cerr << "Sorting failed on line " << line_num << "\n";
            return 1;
        }

        write_sorted_line(mer_out, mer_sorted);
        write_sorted_line(lom_out, lom_sorted);
        write_sorted_line(hoa_out, hoa_sorted);

        trip_out << count_trips_under_budget(mer_sorted, BUDGET) << "\n";
        run_out << "(" << mer_time << ", " << lom_time << ", " << hoa_time << ")\n";
    }

    cout << "Finished benchmarking.\n";
    return 0;
}