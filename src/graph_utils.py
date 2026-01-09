"""
Module xử lý đồ thị, tìm SCC (Strongly Connected Components) bằng Tarjan's Algorithm
và topological sort cho roadmap
"""
from collections import defaultdict, deque
from typing import Any, List, Dict, Set, Tuple


class GraphUtils:
    """Class xử lý đồ thị với Tarjan's Algorithm và topological sort"""
    
    def __init__(self):
        self.graph: Dict[str, List[str]] = defaultdict(list)
        self.in_degree: Dict[str, int] = defaultdict(int)
        self.nodes: Set[str] = set()
        
        # Cho Tarjan's Algorithm
        self.index_counter = 0
        self.stack = []
        self.lowlinks = {}
        self.index = {}
        self.on_stack = {}
        self.sccs = []
        
    def add_edge(self, from_node: str, to_node: str):
        """
        Thêm cạnh vào đồ thị
        
        Args:
            from_node: Node nguồn (prerequisite)
            to_node: Node đích (skill hiện tại)
        """
        self.graph[from_node].append(to_node)
        self.in_degree[to_node] += 1
        self.nodes.add(from_node)
        self.nodes.add(to_node)
        
        # Đảm bảo from_node có entry trong in_degree
        if from_node not in self.in_degree:
            self.in_degree[from_node] = 0
    
    def build_graph(self, items: List[str], get_prerequisites_func, learned_items: Set[str] | None = None):
        """
        Xây dựng đồ thị từ danh sách items và function lấy prerequisites
        Tự động thêm tất cả prerequisites (đệ quy) vào đồ thị
        
        Args:
            items: Danh sách các items cần học
            get_prerequisites_func: Function để lấy prerequisites của một item
            learned_items: Set các items mà user đã học (sẽ không thêm vào graph)
        """
        if learned_items is None:
            learned_items = set()
            
        self.graph.clear()
        self.in_degree.clear()
        self.nodes.clear()
        
        # Set để track các items đã được xử lý (tránh vòng lặp vô hạn)
        processed = set()
        
        def add_item_with_prerequisites(item: str):
            """
            Thêm item và tất cả prerequisites của nó vào đồ thị (đệ quy)
            Bỏ qua các items đã học
            """
            if item in processed or item in learned_items:
                return
            
            processed.add(item)
            
            # Thêm item vào nodes
            self.nodes.add(item)
            if item not in self.in_degree:
                self.in_degree[item] = 0
            
            # Lấy prerequisites
            prerequisites = get_prerequisites_func(item)
            
            for prereq in prerequisites:
                # Nếu prereq đã học, bỏ qua (không thêm vào graph)
                if prereq in learned_items:
                    # print(f"Skipped learned prerequisite: {prereq}")
                    continue
                    
                # Đệ quy thêm prerequisite và các prerequisites của nó
                add_item_with_prerequisites(prereq)
                
                # Thêm edge từ prerequisite đến item
                self.add_edge(prereq, item)
                # print(f"Added edge: ({prereq}) -> ({item})")
        
        # Xử lý tất cả items trong danh sách ban đầu
        for item in items:
            add_item_with_prerequisites(item)
    
    def find_sccs_tarjan(self) -> List[List[str]]:
        """
        Tìm tất cả Strongly Connected Components (SCC) bằng Tarjan's Algorithm
        
        Returns:
            List of SCCs, mỗi SCC là một list các nodes
        """
        self.index_counter = 0
        self.stack = []
        self.lowlinks = {}
        self.index = {}
        self.on_stack = {}
        self.sccs = []
        
        def strongconnect(node: str):
            # Set depth index
            self.index[node] = self.index_counter
            self.lowlinks[node] = self.index_counter
            self.index_counter += 1
            self.stack.append(node)
            self.on_stack[node] = True
            
            # Xét tất cả successors
            successors = self.graph.get(node, [])
            for successor in successors:
                if successor not in self.index:
                    # Successor chưa được thăm, đệ quy
                    strongconnect(successor)
                    self.lowlinks[node] = min(self.lowlinks[node], self.lowlinks[successor])
                elif self.on_stack.get(successor, False):
                    # Successor đang trong stack, là part of current SCC
                    self.lowlinks[node] = min(self.lowlinks[node], self.index[successor])
            
            # Nếu node là root của SCC
            if self.lowlinks[node] == self.index[node]:
                scc = []
                while True:
                    successor = self.stack.pop()
                    self.on_stack[successor] = False
                    scc.append(successor)
                    if successor == node:
                        break
                self.sccs.append(scc)
        
        # Chạy Tarjan cho tất cả nodes chưa thăm
        for node in self.nodes:
            if node not in self.index:
                strongconnect(node)
        
        return self.sccs
    
    def build_condensation_graph(self, sccs: List[List[str]]) -> Tuple[Dict, Dict, Dict]:
        """
        Tạo condensation graph: nén các SCC thành một node duy nhất
        
        Args:
            sccs: List of SCCs từ Tarjan
            
        Returns:
            Tuple of (condensation_graph, scc_map, scc_in_degree)
            - condensation_graph: dict mapping SCC_id -> list of connected SCC_ids
            - scc_map: dict mapping node -> SCC_id
            - scc_in_degree: dict mapping SCC_id -> in_degree
        """
        # Map mỗi node vào SCC_id của nó
        scc_map = {}
        for scc_id, scc in enumerate(sccs):
            for node in scc:
                scc_map[node] = scc_id
        
        # Xây dựng condensation graph
        condensation_graph = defaultdict(set)
        scc_in_degree = defaultdict(int)
        
        # Khởi tạo in_degree cho tất cả SCCs
        for scc_id in range(len(sccs)):
            scc_in_degree[scc_id] = 0
        
        # Duyệt qua tất cả edges trong graph gốc
        for node in self.nodes:
            node_scc = scc_map[node]
            for neighbor in self.graph[node]:
                neighbor_scc = scc_map[neighbor]
                
                # Chỉ thêm edge giữa các SCC khác nhau
                if node_scc != neighbor_scc:
                    if neighbor_scc not in condensation_graph[node_scc]:
                        condensation_graph[node_scc].add(neighbor_scc)
                        scc_in_degree[neighbor_scc] += 1
        
        # Convert sets to lists
        condensation_graph = {k: list(v) for k, v in condensation_graph.items()}
        
        return condensation_graph, scc_map, dict(scc_in_degree)
    
    def topological_sort_dfs_style(self, sccs: List[List[str]], 
                                  condensation_graph: Dict,
                                  scc_in_degree: Dict,
                                  node_levels: Dict[str, int]) -> List[Dict[str, Any]]:
        """
        Topological sort theo DFS style - đi hết một nhánh đến khi gặp node có in_degree > 0
        
        Args:
            sccs: List of SCCs
            condensation_graph: Graph của các SCCs
            scc_in_degree: In-degree của mỗi SCC
            node_levels: Dictionary chứa level của mỗi node
            
        Returns:
            List of stages, mỗi stage chứa thông tin về SCC hoặc sequential path
        """
        result = []
        temp_in_degree = scc_in_degree.copy()
        visited = set()
        
        def dfs_sequential_path(current_scc: int, current_path: List[int]) -> List[int]:
            """
            DFS để tìm sequential path cho đến khi gặp SCC (nhiều nodes) hoặc in_degree > 0
            """
            if current_scc in visited:
                return current_path
                
            visited.add(current_scc)
            current_path.append(current_scc)
            
            # Lấy các neighbors
            neighbors = condensation_graph.get(current_scc, [])
            
            # Nếu có đúng 1 neighbor
            if len(neighbors) == 1:
                neighbor_scc = neighbors[0]

                temp_in_degree[neighbor_scc] -= 1
                
                # QUAN TRỌNG: Nếu neighbor là SCC (nhiều nodes), DỪNG path
                if len(sccs[neighbor_scc]) > 1:
                    return current_path
                
                
                # Chỉ tiếp tục nếu neighbor có in_degree = 0 sau khi trừ VÀ là single node
                if temp_in_degree[neighbor_scc] == 0:
                    return dfs_sequential_path(neighbor_scc, current_path)
            
            elif len(neighbors) > 1:
                # Nhiều hơn 1 neighbor, DỪNG path
                for neighbor_scc in neighbors:
                    temp_in_degree[neighbor_scc] -= 1

            return current_path
        
        # Bắt đầu từ các SCC có in_degree = 0
        queue = deque([scc_id for scc_id in range(len(sccs)) 
                           if temp_in_degree[scc_id] == 0])
        
        # Sắp xếp theo thứ tự để đảm bảo tính ổn định
        queue = deque(sorted(queue))
        # print(f"Zero in-degree SCCs: {list(queue)}")

        while queue:
            start_scc = queue.popleft()
            if start_scc in visited:
                continue
                
            scc_nodes = sccs[start_scc]
            
            # CASE 1: SCC có nhiều nodes (cycle) - học song song
            if len(scc_nodes) > 1:
                scc_nodes_sorted = sorted(scc_nodes, key=lambda x: node_levels.get(x, 5))
                result.append({
                    "type": "scc",
                    "nodes": scc_nodes_sorted,
                    "is_parallel": True,
                    "scc_id": start_scc
                })
                visited.add(start_scc)
                
                # Giảm in_degree của các neighbors
                for neighbor_scc in condensation_graph.get(start_scc, []):
                    temp_in_degree[neighbor_scc] -= 1
                    if temp_in_degree[neighbor_scc] == 0 and neighbor_scc not in visited:
                        queue.append(neighbor_scc)
                    
            # CASE 2: SCC có 1 node - tìm sequential path
            else:
                sequential_path = dfs_sequential_path(start_scc, [])
                
                # Gom tất cả nodes trong sequential path
                ordered_nodes = []
                for scc_id in sequential_path:
                    ordered_nodes.extend(sccs[scc_id])
                
                result.append({
                    "type": "path",
                    "nodes": ordered_nodes,
                    "is_parallel": False,
                    "scc_path": sequential_path
                })

                last_scc = sequential_path[-1]
                for neighbor_scc in condensation_graph.get(last_scc, []):
                    if temp_in_degree[neighbor_scc] == 0 and neighbor_scc not in visited:
                        queue.append(neighbor_scc)
        
        unvisited = set(range(len(sccs))) - visited
        # if unvisited:
        #     print(f"WARNING: Unvisited SCCs detected: {unvisited}")
        #     print(f"This might indicate a cycle in condensation graph!")

        return result
    
    def get_learning_path(self, target_items: List[str], 
                         get_prerequisites_func, 
                         get_level_func,
                         learned_items: Set[str] | None = None) -> Dict[str, Any]:
        """
        Tạo learning path cho các items cần học bằng Tarjan + Topological Sort
        
        Args:
            target_items: Danh sách các items cần học
            get_prerequisites_func: Function để lấy prerequisites
            get_level_func: Function để lấy level của một item
            learned_items: Set các items mà user đã học
            
        Returns:
            Dictionary chứa thông tin về learning path
        """
        # Xây dựng đồ thị (bỏ qua items đã học)
        self.build_graph(target_items, get_prerequisites_func, learned_items)
        
        # Tạo dictionary node_levels cho TẤT CẢ nodes trong graph (bao gồm cả prerequisites)
        node_levels = {node: get_level_func(node) for node in self.nodes}
        
        # Tìm SCCs bằng Tarjan's Algorithm
        sccs = self.find_sccs_tarjan()
        # print(f"📊 Found {len(sccs)} SCCs: {sccs}")
        
        # Xây dựng condensation graph (nén các SCC thành 1 node)
        condensation_graph, scc_map, scc_in_degree = self.build_condensation_graph(sccs)
        
        # In thông tin chi tiết về SCCs và đồ thị sau nén
        # print("\n" + "="*70)
        # print("🔍 CHI TIẾT CÁC SCC (Strongly Connected Components)")
        # print("="*70)
        # for scc_id, scc_nodes in enumerate(sccs):
        #     if len(scc_nodes) > 1:
        #         print(f"SCC {scc_id}: {scc_nodes} (CYCLE - {len(scc_nodes)} nodes)")
        #     else:
        #         print(f"SCC {scc_id}: {scc_nodes}")
        
        # print("\n" + "="*70)
        # print("🗺️  ĐỒ THỊ SAU NÉN (Condensation Graph)")
        # print("="*70)
        # print("Cấu trúc: SCC_id -> [danh sách SCC_id kế tiếp]")
        # for scc_id in range(len(sccs)):
        #     neighbors = condensation_graph.get(scc_id, [])
        #     if neighbors:
        #         # print(f"SCC {scc_id} -> SCC {neighbors}")
        #         for neighbor in neighbors:
        #             print(scc_id, neighbor)
            # else:
            #     print(f"SCC {scc_id} -> [] (không có node kế tiếp)")
        
        # print("\n" + "="*70)
        # print("📊 IN-DEGREE CỦA CÁC SCC")
        # print("="*70)
        # for scc_id in range(len(sccs)):
        #     in_deg = scc_in_degree.get(scc_id, 0)
        #     status = "START" if in_deg == 0 else ""
            # print(f"SCC {scc_id}: in-degree = {in_deg} {status}")
        # print("="*70 + "\n")
        
        # Topological sort theo DFS style
        learning_path = self.topological_sort_dfs_style(
            sccs, condensation_graph, scc_in_degree, node_levels
        )
        # print(f"🎯 Learning path: {learning_path}")
        
        # Tìm các SCCs có nhiều hơn 1 node (có cycle)
        cycles_info = []
        for scc in sccs:
            if len(scc) > 1:
                cycles_info.append(scc)
        
        return {
            "path": learning_path,
            "has_cycles": len(cycles_info) > 0,
            "cycles": cycles_info,
            "sccs": sccs,
            "total_items": len(self.nodes)  # Đếm tất cả nodes trong graph (chưa học)
        }
    
    def get_parallel_learning_groups(self, learning_path: List[Dict]) -> List[Dict[str, Any]]:
        """
        Chuyển đổi learning path thành format dễ hiểu hơn cho roadmap
        
        Args:
            learning_path: Kết quả từ topological_sort_dfs_style
            
        Returns:
            List of dictionaries với thông tin từng stage
        """
        result: List[Dict[str, Any]] = []
        stage_num = 1
        
        for path_item in learning_path:
            nodes = path_item["nodes"]
            is_parallel = path_item["is_parallel"]
            
            result.append({
                "stage": stage_num,
                "items": nodes,
                "count": len(nodes),
                "can_learn_parallel": is_parallel,
                "is_scc": path_item["type"] == "scc",
                "type": path_item["type"]
            })
            stage_num += 1
        
        return result

