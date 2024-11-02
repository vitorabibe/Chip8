import os

def findCh8Files(fileType, paths):
    if len(paths) == 0:
        return []
    _, extension = os.path.splitext(paths[0])
    print(paths)
    print(extension)
    nextPaths = findCh8Files(fileType, paths[1:])
    if fileType == extension:
        return [paths[0]] + nextPaths
    else:
        return nextPaths

def findFolderDir(folder, path):
    if folder in path:
        return path
    else:
        try:
            for directory in os.listdir(path):
                newPath = os.path.join(path, directory)
                if os.path.isdir(newPath):
                    nextPath = findFolderDir(folder, newPath)
                    if nextPath != None:
                        return nextPath
        except PermissionError:
            pass
        return None

def findPaths(folder):
    result = []
    folderDir = findFolderDir(folder, '/Users')
    for file in os.listdir(folderDir):
        result.append(file)
    return result


print(findCh8Files('.ch8', findPaths('Chip 8')))


