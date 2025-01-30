import subprocess
from pathlib import Path
from typing import Optional, List
import platform
import os

class CommandExecutor:
    """시스템 명령어 실행을 처리하는 클래스"""

    def __init__(self, root_path: str):
        self.root_path = Path(root_path)

    def execute_command(self, command: str) -> tuple[str, str]:
        """명령어 실행

        Args:
            command (str): 실행할 명령어

        Returns:
            tuple[str, str]: (표준 출력, 표준 에러)
        """
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                shell=True
            )
            return result.stdout, result.stderr
        except Exception as e:
            return "", str(e)

    def cmd_tree(self) -> tuple[str, str]:
        """CMD tree 명령어로 트리 구조 출력"""
        command = f'tree "{self.root_path}" /F'
        return self.execute_command(command)

    def ps_tree(self) -> tuple[str, str]:
        """PowerShell로 트리 구조 출력"""
        command = f'powershell "Get-ChildItem -Path \'{self.root_path}\' -Recurse | Select-Object FullName"'
        return self.execute_command(command)

    def ps_tree_extensions(self, extensions: Optional[List[str]] = None) -> tuple[str, str]:
        """PowerShell로 선택된 확장자의 파일만 출력

        Args:
            extensions (Optional[List[str]], optional): 표시할 확장자 목록. Defaults to None.

        Returns:
            tuple[str, str]: (표준 출력, 표준 에러)
        """
        if not extensions:
            return self.ps_tree()

        extension_filter = ','.join(f'*{ext}' for ext in extensions)
        command = f'powershell "Get-ChildItem -Path \'{self.root_path}\' -Recurse -Include {extension_filter} | Select-Object FullName"'
        return self.execute_command(command)

    def open_folder(self, folder_path: str) -> bool:
        """폴더를 시스템 파일 탐색기로 열기

        Args:
            folder_path (str): 열 폴더 경로

        Returns:
            bool: 성공 여부
        """
        try:
            if not os.path.exists(folder_path):
                return False

            if platform.system() == "Windows":
                os.startfile(folder_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.Popen(["open", folder_path])
            else:  # Linux and other Unix-like
                subprocess.Popen(["xdg-open", folder_path])
            return True
        except Exception:
            return False